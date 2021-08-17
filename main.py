import collections
import statistics

import os
import xmltodict
from bottle import route, run, view, request, static_file, get
import urllib.request


def make_int(number):
    if number:
        return int(number) if number.isnumeric() else 0
    return


def make_float(number):
    try:
        float(number)
        return round(float(number), 1)
    except:
        return


def calc_diff(left, right):
    try:
        if left > 0 and right > 0:
            return abs(left-right)
        return
    except:
        return


def create_user_collection(username):
    loading_status = list()
    api_result = request_user_collection(["username="+username])
    collection = collections.OrderedDict()
    if "message" in api_result:
        loading_status.append({"username": username, "status": 0, "message": api_result.get("message", "")})
    elif "errors" in api_result:
        try:
            loading_status.append({"username": username, "status": 0, "errors": api_result.get("errors").get("error").get("message")})
        except:
            loading_status.append({"username": username, "status": 0, "message": "Unknown error"})
    elif "items" in api_result:
        try:
            total_items = 0
            match_items_comment = 0
            for item in api_result.get("items").get("item"):

                total_items += 1
                collection[item["@objectid"]] = {
                    "type": item.get("@subtype", ""),
                    "name": item.get("originalname", ""),
                    "display_name": item.get("name", "").get("#text", ""),
                    "yearpublished": item.get("yearpublished", ""),
                    "thumbnail": item.get("thumbnail", ""),
                    "stats": {
                        "minplayers": make_int(item.get("stats").get("@minplayers", None)),
                        "maxplayers": make_int(item.get("stats").get("@maxplayers", None)),
                        "minplaytime": make_int(item.get("stats").get("@minplaytime", None)),
                        "maxplaytime": make_int(item.get("stats").get("@maxplaytime", None)),
                        "numowned": make_int(item.get("stats").get("@numowned", None)),
                        "numrating": make_int(item.get("stats").get("rating").get("usersrated").get("@value", None)),
                        "average": make_float(item.get("stats").get("rating").get("average").get("@value", None)),
                        "bayesaverage": make_float(item.get("stats").get("rating").get("bayesaverage").get("@value", None)),
                    },
                    "users": {
                        username: {
                            "rating": make_int(item.get("stats").get("rating").get("@value", None)),
                            "diff_rating": None,
                            "numplays": make_int(item.get("numplays", None)),
                            "comment": item.get("comment", ""),
                            "status": {
                                "own": item.get("status").get("@own", 0),
                                "prevowned": item.get("status").get("@prevowned", 0),
                                "fortrade": item.get("status").get("@fortrade", 0),
                                "want": item.get("status").get("@want", 0),
                                "wanttoplay": item.get("status").get("@wanttoplay", 0),
                                "wanttobuy": item.get("status").get("@wanttobuy", 0),
                                "wishlist": item.get("status").get("@wishlist", 0),
                                "preordered": item.get("status").get("@preordered", 0),
                                "lastmodified": item.get("status").get("@lastmodified", 0),
                            }
                        }
                    },
                    "user": {
                        "rating": make_int(item.get("stats").get("rating").get("@value", None)),
                        "numplays": make_int(item.get("numplays", None)),
                        "comment": item.get("comment", ""),
                        "status": {
                            "own": item.get("status").get("@own", 0),
                            "prevowned": item.get("status").get("@prevowned", 0),
                            "fortrade": item.get("status").get("@fortrade", 0),
                            "want": item.get("status").get("@want", 0),
                            "wanttoplay": item.get("status").get("@wanttoplay", 0),
                            "wanttobuy": item.get("status").get("@wanttobuy", 0),
                            "wishlist": item.get("status").get("@wishlist", 0),
                            "preordered": item.get("status").get("@preordered", 0),
                            "lastmodified": item.get("status").get("@lastmodified", 0),
                        }
                    }
                }
                if item.get("comment"):
                    match_items_comment += 1
            loading_status.append({
                "username": username,
                "status": 1,
                "total_items": total_items,
                "match_items": 0,
                "match_items_comment": match_items_comment,
            })
        except:
            loading_status.append({"username": username, "status": 0, "message": "Unknown error"})

    return collection, loading_status


def add_user_to_collection(collection, loading_status, username):
    api_result = request_user_collection(["username="+username, "rated=1"])
    if "message" in api_result:
        loading_status.append({"username": username, "status": 0, "message": api_result.get("message", "")})
    elif "errors" in api_result:
        try:
            loading_status.append({"username": username, "status": 0, "errors": api_result.get("errors").get("error").get("message")})
        except:
            loading_status.append({"username": username, "status": 0, "message": "Unknown error"})
    elif "items" in api_result:
        try:
            diff_ratings = list()
            total_items = 0
            match_items = 0
            match_items_comment = 0
            if make_int(api_result.get("items").get("@totalitems")) > 0:
                for item in api_result.get("items").get("item"):
                    total_items += 1
                    if item["@objectid"] in collection.keys():
                        match_items += 1
                        diff_rating = calc_diff(make_int(item.get("stats").get("rating").get("@value", None)), collection[item["@objectid"]]["user"]["rating"])
                        collection[item["@objectid"]]["users"][username] = {
                            "rating": make_int(item.get("stats").get("rating").get("@value", None)),
                            "diff_rating": diff_rating,
                            "numplays": make_int(item.get("numplays", None)),
                            "comment": item.get("comment", ""),
                            "status": {
                                "own": item.get("status").get("@own", 0),
                                "prevowned": item.get("status").get("@prevowned", 0),
                                "fortrade": item.get("status").get("@fortrade", 0),
                                "want": item.get("status").get("@want", 0),
                                "wanttoplay": item.get("status").get("@wanttoplay", 0),
                                "wanttobuy": item.get("status").get("@wanttobuy", 0),
                                "wishlist": item.get("status").get("@wishlist", 0),
                                "preordered": item.get("status").get("@preordered", 0),
                                "lastmodified": item.get("status").get("@lastmodified", 0),
                            }
                        }
                        if item.get("comment"):
                            match_items_comment += 1
                        if diff_rating:
                            diff_ratings.append(diff_rating)
            loading_status.append({
                "username": username,
                "status": 1,
                "mean_diff_rating": make_float(statistics.mean(diff_ratings)),
                "total_items": total_items,
                "match_items": match_items,
                "match_items_comment": match_items_comment,
            })
        except:
            loading_status.append({"username": username, "status": 0})

    return collection, loading_status


def request_user_collection(params):
    try:
        param_str = "&".join(params).replace(" ", "%20")
        with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/collection?stats=1&" + param_str) as response:
            xml = response.read()
        return xmltodict.parse(xml)
    except:
        return


def calc_ratings(collection):
    for _, item in collection.items():
        ratings = list()
        diff_ratings = list()
        numplays = list()
        for _, user in item["users"].items():
            if user["rating"] in range(1, 11):
                ratings.append(user["rating"])
            if user["diff_rating"] in range(1, 11):
                diff_ratings.append(user["diff_rating"])
            if user["numplays"]:
                numplays.append(user["numplays"])
        item["calc"] = {
            "mean_rating": make_float(statistics.mean(ratings)) if ratings else 0,
            "mean_diff_rating": make_float(statistics.mean(diff_ratings)) if diff_ratings else 0,
            "median_rating": make_float(statistics.median(ratings)) if ratings else 0,
            "sum_numplays": sum(numplays),
        }
    return collection


def build_collection_url(loading_status):
    for main_user in loading_status:
        collection_url = main_user["username"]
        remove_collection_url = ""
        for key, user in enumerate(loading_status):
            if key == 0:
                collection_url += "?add_user="+user["username"]
            elif user["username"] != main_user["username"]:
                collection_url += "&add_user="+user["username"]
        for key, user in enumerate([i for i in loading_status if not (i['username'] == main_user["username"])]):
            if key == 0:
                remove_collection_url += user["username"]
            else:
                remove_collection_url += "?add_user="+user["username"]

        main_user["collection_url"] = collection_url
        main_user["remove_collection_url"] = remove_collection_url
    return loading_status


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/')


@route("/")
@route("/bgg/<username>")
@view("views/result")
def bgg(username="locou"):
    collection, loading_status = create_user_collection(username)
    users_to_compare = request.GET.getall('add_user')
    if users_to_compare:
        for user_to_compare in users_to_compare:
            collection, loading_status = add_user_to_collection(collection, loading_status, user_to_compare)
    collection = calc_ratings(collection)
    loading_status = build_collection_url(loading_status)
    return dict(collection=collection, loading_status=loading_status)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)
