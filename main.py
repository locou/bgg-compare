import os

from bgg_collection import calc_ratings, build_collection_url, add_user_to_collection, create_user_collection
from database import get_cached_usernames
from bottle import route, run, view, request, static_file, get


@get('/<filename:re:.*(\.css|\.js)>')
def stylesheets(filename):
    return static_file(filename, root='static/')


@route("/cache")
@view("views/cache")
def cache():
    result = get_cached_usernames()
    return dict(result=result)


@route("/")
@view("views/index")
def index():
    # TODO: welcome page + select a username
    return {}


@route("/<username>")
@route("/bgg/<username>")
@view("views/result")
def bgg(username):
    collection, loading_status = create_user_collection(username)
    users_to_compare = request.GET.getall('add_user')
    if users_to_compare:
        for user_to_compare in users_to_compare:
            collection, loading_status = add_user_to_collection(collection, loading_status, user_to_compare)
    collection = calc_ratings(collection)
    sort_by = request.GET.get('sort_by')
    # TODO: sort by my_rating by default
    if sort_by:
        if "ASC" in sort_by:
            order_by = False
        else:
            order_by = True
        if "boardgame_numowned" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("stats").get("numowned"), reverse=order_by))
        elif "boardgame_rating" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("stats").get("average"), reverse=order_by))
        elif "boardgame_title" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("display_name"), reverse=order_by))
        elif "boardgame_year" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("yearpublished"), reverse=order_by))
        elif "my_rating" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("user").get("rating"), reverse=order_by))
        elif "my_numplays" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("user").get("numplays"), reverse=order_by))
        elif "combined_numplays" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("calc").get("sum_numplays"), reverse=order_by))
            for key in list(collection):
                if collection[key].get("calc").get("sum_numplays") == 0:
                    del collection[key]
        elif "combined_mean_rating" in sort_by:
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("calc").get("mean_rating"), reverse=order_by))
            for key in list(collection):
                if collection[key].get("calc").get("mean_rating") == 0:
                    del collection[key]
        elif "combined_mean_diff_rating" in sort_by:
            for key in list(collection):
                if collection[key].get("calc").get("mean_diff_rating") is None:
                    del collection[key]
            collection = dict(sorted(collection.items(), key=lambda item: item[1].get("calc").get("mean_diff_rating"), reverse=order_by))
    loading_status = build_collection_url(loading_status)
    return dict(collection=collection, loading_status=loading_status)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8081, debug=True, reloader=True)
