import collections
import statistics
from datetime import datetime

from database import get_or_create_collection


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
    result = get_or_create_collection(username)
    collection = collections.OrderedDict()
    if result["message"]["status"] == 0:
        loading_status.append(result["message"])
    elif result["message"]["status"] == 1 and "item" in result["collection"]["items"]:
        try:
            total_items = 0
            match_items_comment = 0
            if isinstance(result["collection"].get("items").get("item"), dict):
                result["collection"]["items"]["item"] = [result["collection"].get("items").get("item")]
            for item in result["collection"].get("items").get("item"):

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
                                "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0), '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
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
    result = get_or_create_collection(username)
    if result["message"]["status"] == 0:
        loading_status.append(result["message"])
    elif result["message"]["status"] == 1:
        try:
            diff_ratings = list()
            total_items = 0
            match_items = 0
            match_items_comment = 0
            if make_int(result["collection"].get("items").get("@totalitems")) > 0:
                for item in result["collection"].get("items").get("item"):
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
                                "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0), '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
                            }
                        }
                        if item.get("comment"):
                            match_items_comment += 1
                        if isinstance(diff_rating, int) and diff_rating >= 0:
                            diff_ratings.append(diff_rating)

            loading_status.append({
                "username": username,
                "status": 1,
                "mean_diff_rating": make_float(statistics.mean(diff_ratings)) if len(diff_ratings) > 0 else None,
                "diff_ratings": sorted(diff_ratings),
                "total_items": total_items,
                "match_items": match_items,
                "match_items_comment": match_items_comment,
            })
        except TypeError:
            loading_status.append({"username": username, "status": 0})

    return collection, loading_status


def calc_ratings(collection):
    for _, item in collection.items():
        ratings = list()
        diff_ratings = list()
        numplays = list()
        for _, user in item["users"].items():
            if user["rating"] in range(1, 11):
                ratings.append(user["rating"])
            if user["diff_rating"] in range(0, 10):
                diff_ratings.append(user["diff_rating"])
            if user["numplays"]:
                numplays.append(user["numplays"])
        item["calc"] = {
            "mean_rating": make_float(statistics.mean(ratings)) if ratings else None,
            "mean_diff_rating": make_float(statistics.mean(diff_ratings)) if diff_ratings else None,
            "median_rating": make_float(statistics.median(ratings)) if ratings else None,
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