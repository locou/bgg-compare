import collections
import statistics
from datetime import datetime

from database import get_or_create_collection


def make_int(number):
    try:
        float(number)
        return int(float(number))
    except:
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


def get_title(originalname, name, type):
    if type == "title":
        return originalname if originalname != "" else name
    elif type == "alternative_title":
        return name if originalname != "" else ""


def build_url(user_list):
    url = ""
    for key, username in enumerate(user_list):
        if key == 0:
            url += username
        elif key == 1:
            url += "?add_user=" + username
        else:
            url += "&add_user=" + username
    return url


def create_user_collection(username):
    loading_status = list()
    result = get_or_create_collection(username)
    collection = collections.OrderedDict()
    if result["message"]["status"] == 0:
        loading_status.append(result["message"])
    elif result["message"]["status"] == 1 and "item" not in result["collection"]["items"]:
        loading_status.append({
            "username": username,
            "status": 1,
            "total_items": 0,
            "match_items": 0,
            "match_items_comment": 0,
        })
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
                    "title": get_title(item.get("originalname", ""), item.get("name").get("#text", ""), "title"),
                    "alternative_title": get_title(item.get("originalname", ""), item.get("name").get("#text", ""), "alternative_title"),
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
            total_items_comment = 0
            if make_int(result["collection"].get("items").get("@totalitems")) > 0:
                for item in result["collection"].get("items").get("item"):
                    total_items += 1
                    if item.get("comment"):
                        total_items_comment += 1
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
                            title = get_title(item.get("originalname", ""), item.get("name").get("#text", ""), "title")
                            diff_ratings.append({"title": title, "diff_rating": diff_rating})

            loading_status.append({
                "username": username,
                "status": 1,
                "updated_at": datetime.strftime(result["message"]["updated_at"], "%Y-%m-%d"),
                "mean_diff_rating": make_float(statistics.mean([i["diff_rating"] for i in diff_ratings])) if len(diff_ratings) > 0 else None,
                "diff_ratings":  sorted(diff_ratings, key=lambda item: item["diff_rating"]),
                "total_items": total_items,
                "match_items": match_items,
                "match_items_comment": match_items_comment,
                "total_items_comment": total_items_comment,
            })
        except TypeError:
            loading_status.append({"username": username, "status": 0})

    return collection, loading_status


def calc_ratings(collection):
    for _, item in collection.items():
        ratings = list()
        diff_ratings = list()
        numplays = list()
        count_comments = 0
        count_ratings = 0
        count_users = 0
        for _, user in item["users"].items():
            if user["rating"] in range(1, 11):
                ratings.append(user["rating"])
                count_ratings += 1
            if user["diff_rating"] in range(0, 10):
                diff_ratings.append(user["diff_rating"])
            if user["numplays"]:
                numplays.append(user["numplays"])
            if user["comment"]:
                count_comments += 1
            count_users += 1

        item["calc"] = {
            "mean_rating": make_float(statistics.mean(ratings)) if ratings else None,
            "mean_diff_rating": make_float(statistics.mean(diff_ratings)) if len(diff_ratings) > 0 else None,
            "median_rating": make_float(statistics.median(ratings)) if ratings else None,
            "sum_numplays": sum(numplays),
            "count_comments": count_comments,
            "count_ratings": count_ratings,
            "count_users": count_users,
        }
    return collection


def build_collection_url(loading_status):
    if len(loading_status) > 1:
        for user_status in loading_status:

            # move the user to the front of the list
            user_list = [u["username"] for u in loading_status]
            user_list.insert(0, user_list.pop(user_list.index(user_status["username"])))

            # remove user from list
            remove_list = [u["username"] for u in loading_status]
            remove_list.pop(remove_list.index(user_status["username"]))
            user_status["collection_url"] = build_url(user_list)
            user_status["remove_collection_url"] = build_url(remove_list)
        return loading_status
    elif loading_status:
        loading_status[0]["collection_url"] = None
        loading_status[0]["remove_collection_url"] = None
    return loading_status
