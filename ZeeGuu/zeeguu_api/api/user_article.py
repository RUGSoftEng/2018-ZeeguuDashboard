import flask
import zeeguu
from flask import request
from zeeguu.content_recommender.mixed_recommender import user_article_info
from zeeguu.model import Article, UserArticle

from .utils.route_wrappers import cross_domain, with_session
from .utils.json_result import json_result
from . import api

session = zeeguu.db.session


# ---------------------------------------------------------------------------
@api.route("/user_article", methods=("GET",))
# ---------------------------------------------------------------------------
@cross_domain
@with_session
def user_article():
    """

        called user_article because it returns info about the article
        but also the user-specific data relative to the article

        takes url as URL argument
        NOTE: the url should be encoded with quote_plus (Pyton) and encodeURIComponent(Javascript)

        this is not perfectly RESTful, but we're not fundamentalist...
        and currently we want to have the url as the URI for the article
        and for some reason if we put the uri as part of the path,
        apache decodes it before we get it in here.
        so for now, we're just not putting it as part of the path


    :return: json as prepared by content_recommender.mixed_recommender.user_article_info

    """

    url = request.args.get('url', '')
    if not url:
        flask.abort(400)

    article = Article.find_or_create(session, url)

    return json_result(user_article_info(flask.g.user, article, with_content=True))


# ---------------------------------------------------------------------------
@api.route("/user_article", methods=("POST",))
# ---------------------------------------------------------------------------
@cross_domain
@with_session
def user_article_update():
    """

        update info about this (user x article) pair
        in the form data you can provide
        - liked=True|1|False|0
        - starred -ibidem-

    :return: json as prepared by content_recommender.mixed_recommender.user_article_info

    """

    url = request.form.get('url')
    starred = request.form.get('starred')
    liked = request.form.get('liked')

    article = Article.find_or_create(session, url)
    user_article = UserArticle.find_or_create(session, flask.g.user, article)

    if starred is not None:
        user_article.set_starred(starred in ["True", "1"])

    if liked is not None:
        user_article.set_liked(liked in ["True", "1"])

    session.commit()

    return "OK"


# ---------------------------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!! DEPRECATED !!!!!!!!!!!!!!!!!!!!!!!!!
@api.route("/get_user_article_info", methods=("POST",))
# !!!!!!!!!!!!!!!!!!!!!!!!! DEPRECATED !!!!!!!!!!!!!!!!!!!!!!!!!
# ---------------------------------------------------------------------------
@cross_domain
@with_session
def get_user_article_info():
    """

        expects one parameter: url

    :return: json dictionary with info

    """

    url = str(request.form.get('url', ''))

    article = Article.find_or_create(session, url)

    return json_result(user_article_info(flask.g.user, article))
