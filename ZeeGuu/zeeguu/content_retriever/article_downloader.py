"""

    Goes through all the interesting sources that the server knows
    about and downloads new articles saving them in the DB.  


"""
from datetime import datetime

import watchmen
import zeeguu

from zeeguu import model
from zeeguu.model import Url, RSSFeed, Article, Topic
from zeeguu.constants import SIMPLE_TIME_FORMAT

LOG_CONTEXT = "FEED RETRIEVAL"


def download_from_feed(feed: RSSFeed, session, limit=1000):
    """

        Session is needed because this saves stuff to the DB.


        last_crawled_time is useful because otherwise there would be a lot of time
        wasted trying to retrieve the same articles, especially the ones which
        can't be retrieved, so they won't be cached.


    """
    zeeguu.log(feed)
    downloaded = 0
    skipped = 0
    skipped_too_short = 0
    skipped_already_in_db = 0

    last_retrieval_time_from_DB = None
    last_retrieval_time_seen_this_crawl = None

    if feed.last_crawled_time:
        last_retrieval_time_from_DB = feed.last_crawled_time
        zeeguu.log(f"last retrieval time from DB = {last_retrieval_time_from_DB}")

    for feed_item in feed.feed_items():

        if downloaded >= limit:
            break

        url = feed_item['url']

        try:
            this_article_time = datetime.strptime(feed_item['published'], SIMPLE_TIME_FORMAT)
            this_article_time = this_article_time.replace(tzinfo=None)
        except:
            print(f"can't get time from {url}: {feed_item['published']}")
            continue

        if last_retrieval_time_from_DB:

            if this_article_time < last_retrieval_time_from_DB:
                skipped += 1
                continue

        title = feed_item['title']
        summary = feed_item['summary']

        art = model.Article.find(url)

        if (not last_retrieval_time_seen_this_crawl) or (this_article_time > last_retrieval_time_seen_this_crawl):
            last_retrieval_time_seen_this_crawl = this_article_time

        if art:
            skipped_already_in_db += 1
        else:
            try:
                art = watchmen.article_parser.get_article(url)

                word_count = len(art.text.split(" "))

                if word_count < Article.MINIMUM_WORD_COUNT:
                    skipped_too_short += 1
                else:
                    from zeeguu.language.difficulty_estimator_factory import DifficultyEstimatorFactory

                    # Create new article and save it to DB
                    new_article = zeeguu.model.Article(
                        Url.find_or_create(session, url),
                        title,
                        ', '.join(art.authors),
                        art.text,
                        summary,
                        this_article_time,
                        feed,
                        feed.language
                    )
                    session.add(new_article)
                    session.commit()
                    downloaded += 1

                    for each in Topic.query.all():
                        if each.language == new_article.language and each.matches_article(new_article):
                            new_article.add_topic(each)
            except:
                import sys
                ex = sys.exc_info()[0]
                zeeguu.log(f" {LOG_CONTEXT}: Failed to create zeeguu.Article from {url}\n{str(ex)}")

    zeeguu.log(f'  Skipped due to time: {skipped} ')
    zeeguu.log(f'  Downloaded: {downloaded}')
    zeeguu.log(f'  Too short: {skipped_too_short}')
    zeeguu.log(f'  Already in DB: {skipped_already_in_db}')

    if last_retrieval_time_seen_this_crawl:
        feed.last_crawled_time = last_retrieval_time_seen_this_crawl
    session.add(feed)
    session.commit()
