import os
import random

from datetime import datetime
from bgg_collection import calc_ratings, build_url, build_collection_url, add_user_to_collection, create_user_collection
from bgg_request import handle_user_request
from database import get_cached_usernames, refresh_collection_cache
from bottle import route, run, view, request, static_file, get, redirect, post


@get('/<filename:re:.*(\.css|\.js)>')
def stylesheets(filename):
    return static_file(filename, root='static/')


@route("/cache")
@view("views/cache")
def cache():
    result = get_cached_usernames()
    for user in result:
        if divmod((datetime.now() - datetime.strptime(user['updated_at'], "%Y-%m-%d")).total_seconds(), 3600)[0] > int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS", 0)):
            user["expired"] = 1
        else:
            user["expired"] = 0
    return dict(result=result)


@route("/")
@view("views/index")
def index():
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
    if request.POST.get('refresh_cache'):
        refresh_collection_cache(user)
    if request.POST.get('include_random_users'):
        query_users = [u.username for u in get_cached_usernames(exclude_usernames=users)]
        random.shuffle(query_users)
        users = users + query_users[:5]
    parameters = list()
    for user in users:
        parameters.append((user, "add_user"))
    for etag in request.POST.getall('exclude'):
        parameters.append((etag, "exclude"))
    if request.POST.get('exclude_tag_own'):
        parameters.append(("own", "exclude"))
    if request.POST.get('exclude_tag_prevowned'):
        parameters.append(("prevowned", "exclude"))
    if request.POST.get('exclude_tag_preordered'):
        parameters.append(("preordered", "exclude"))
    if request.POST.get('exclude_tag_wishlist1'):
        parameters.append(("wishlist1", "exclude"))
    if request.POST.get('exclude_tag_wishlist2'):
        parameters.append(("wishlist2", "exclude"))
    if request.POST.get('exclude_tag_wishlist3'):
        parameters.append(("wishlist3", "exclude"))
    if request.POST.get('exclude_tag_wishlist4'):
        parameters.append(("wishlist4", "exclude"))
    if request.POST.get('exclude_tag_wishlist5'):
        parameters.append(("wishlist5", "exclude"))
    if request.POST.get('exclude_tag_fortrade'):
        parameters.append(("fortrade", "exclude"))
    if request.POST.get('exclude_tag_want'):
        parameters.append(("want", "exclude"))
    if request.POST.get('exclude_tag_wanttoplay'):
        parameters.append(("wanttoplay", "exclude"))
    if request.POST.get('exclude_tag_wanttobuy'):
        parameters.append(("wanttobuy", "exclude"))
    if request.POST.get('exclude_tag_notag'):
        parameters.append(("notag", "exclude"))
    if request.POST.get('exclude_tag_boardgame'):
        parameters.append(("boardgame", "exclude"))
    if request.POST.get('exclude_tag_boardgameexpansion'):
        parameters.append(("boardgameexpansion", "exclude"))
    if request.POST.get('exclude_tag_norating'):
        parameters.append(("norating", "exclude"))
    if request.POST.get('exclude_tag_nocomment'):
        parameters.append(("nocomment", "exclude"))
    if request.POST.get('exclude_tag_noplays'):
        parameters.append(("noplays", "exclude"))
    redirect("/bgg/"+build_url(parameters))


@route("/bgg/<username>")
@view("views/result")
def bgg(username):
    exclude_tags = request.GET.getall('exclude')
    collection, loading_status = create_user_collection(username, exclude_tags)
    users_to_compare = request.GET.getall('add_user')
    if users_to_compare:
        for user_to_compare in users_to_compare:
            collection, loading_status = add_user_to_collection(collection, loading_status, user_to_compare)
    collection = calc_ratings(collection)

    loading_status = build_collection_url(loading_status, exclude_tags)
    loading_status = sorted(loading_status, key=lambda k: 11 if k.get('mean_diff_rating', 11) is None else k.get('mean_diff_rating', 11))

    # Sort collection by rating
    collection = dict(sorted(collection.items(), key=lambda item: (-1 if item[1].get("user").get("rating") is None else item[1].get("user").get("rating")), reverse=True))

    # TODO: keep hard filters when switching to another collection
    return dict(collection=collection, loading_status=loading_status, main_user=loading_status[0], exclude_tags=exclude_tags)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8081, debug=True)
