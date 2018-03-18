"""

 Recommends a mix of articles from all the sources


"""
from zeeguu import log
from zeeguu.model import RSSFeedRegistration, UserArticle, Article, User, Bookmark


def user_article_info(user: User, article: Article, with_content=False):
    prior_info = UserArticle.find(user, article)

    ua_info = article.article_info(with_content=with_content)

    if not prior_info:
        ua_info['starred'] = False
        ua_info['opened'] = False
        ua_info['liked'] = False
        ua_info['translations'] = []
        return ua_info

    ua_info['starred'] = prior_info.starred is not None
    ua_info['opened'] = prior_info.opened is not None
    ua_info['liked'] = prior_info.liked

    translations = Bookmark.find_all_for_user_and_url(user, article.url)
    ua_info['translations'] = [each.serializable_dictionary() for each in translations]

    return ua_info


def article_recommendations_for_user(user, count):
    """

            Retrieve :param count articles which are equally distributed
            over all the feeds to which the :param user is registered to.

    :return:

    """

    all_user_registrations = RSSFeedRegistration.feeds_for_user(user)
    per_feed_count = int(count / len(all_user_registrations)) + 1

    all_articles = []
    for registration in all_user_registrations:
        feed = registration.rss_feed
        log(f'Getting articles for {feed}')
        new_articles = feed.get_articles(user, limit=per_feed_count, most_recent_first=True)
        all_articles.extend(new_articles)
        log(f'Added articles for {feed}')

    log('Sorting articles...')
    all_articles.sort(key=lambda each: each.published_time, reverse=True)
    log('Sorted articles')

    return [user_article_info(user, article) for article in all_articles[:count]]
