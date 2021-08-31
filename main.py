import os
import random

from bgg_collection import calc_ratings, build_url, build_collection_url, add_user_to_collection, create_user_collection
from bgg_request import handle_user_request
from database import get_cached_usernames
from bottle import route, run, view, request, static_file, get, redirect, post


@get('/<filename:re:.*(\.css|\.js)>')
def stylesheets(filename):
    return static_file(filename, root='static/')


@route("/cache")
@view("views/cache")
def cache():
    # TODO: remove this page?
    result = get_cached_usernames()
    return dict(result=result)


@route("/")
@view("views/index")
def index():
    # TODO: checkmark to refresh the cache
    return dict(cache_hours=int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS", 0)))


@post("/process")
def process():
    user = request.POST.get('main_user')
    users = request.POST.getall('add_user')
    if request.POST.get('include_buddies'):
        # TODO: include all cached buddies + x random ones, which are not cached
        # TODO: make number of buddies a constant and display it in the ui
        for buddy in handle_user_request(user)[:5]:
            users.append(buddy)
    users = list(set(users))
    users.insert(0, user)
    if request.POST.get('include_random_users'):
        query_users = [u.username for u in get_cached_usernames(exclude_usernames=users)]
        random.shuffle(query_users)
        users = users + query_users[:5]
    redirect("/bgg/"+build_url(users))


@route("/bgg/<username>")
@view("views/result")
def bgg(username):
    collection, loading_status = create_user_collection(username)
    users_to_compare = request.GET.getall('add_user')
    if users_to_compare:
        for user_to_compare in users_to_compare:
            collection, loading_status = add_user_to_collection(collection, loading_status, user_to_compare)
    collection = calc_ratings(collection)

    loading_status = build_collection_url(loading_status)

    # TODO: show cache date
    # TODO: pagination for big collections
    return dict(collection=collection, loading_status=loading_status, main_user=username)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8081, debug=True)
