import collections
import statistics
from datetime import datetime

from database import get_or_create_collection, get_or_create_games


def make_int(number):
    try:
        float(number)
        return int(float(number))
    except:
        return


def make_float(number, decimals=1):
    try:
        float(number)
        return round(float(number), decimals)
    except:
        return


def calc_diff(left, right):
    try:
        if left > 0 and right > 0:
            return abs(left - right)
        return
    except:
        return


def get_title(originalname, name, type):
    if type == "title":
        return originalname if originalname != "" else name
    elif type == "alternative_title":
        return name if originalname != "" else ""


def build_url(parameters):
    # first entry has to be a username
    url = ""
    for key, parameter in enumerate(parameters):
        if key == 0:
            url += parameter[0]
        elif key == 1:
            url += "?" + parameter[1] + "=" + parameter[0]
        else:
            url += "&" + parameter[1] + "=" + parameter[0]
    return url


def create_user_collection(username, paramenters):
    loading_status = list()
    result = get_or_create_collection(username)
    collection = collections.OrderedDict()
    if result["message"]["status"] == 0:
        loading_status.append(result["message"])
    elif result["message"]["status"] == 1 and "item" not in result["collection"]["items"]:
        loading_status.append({
            "username": username,
            "status": 1,
            "updated_at": datetime.strftime(result["message"]["updated_at"], "%Y-%m-%d"),
            "total_items": 0,
            "match_items": 0,
            "match_items_rating": 0,
            "match_items_comment": 0,
            "mean_diff_rating": -100,
        })
    elif result["message"]["status"] == 1 and "item" in result["collection"]["items"]:
        try:
            if isinstance(result["collection"].get("items").get("item"), dict):
                result["collection"]["items"]["item"] = [result["collection"].get("items").get("item")]
            game_ids = list()
            for item in result["collection"].get("items").get("item"):
                game_ids.append(item["@objectid"])
            games = get_or_create_games(game_ids)
            total_items = 0
            match_items_rating = 0
            match_items_comment = 0
            for item in result["collection"].get("items").get("item"):
                game = games.get(int(item["@objectid"]))
                user_tags = list()
                if item.get("status").get("@own") == "1":
                    user_tags.append("own")
                if item.get("status").get("@prevowned") == "1":
                    user_tags.append("prevowned")
                if item.get("status").get("@fortrade") == "1":
                    user_tags.append("fortrade")
                if item.get("status").get("@want") == "1":
                    user_tags.append("want")
                if item.get("status").get("@wanttoplay") == "1":
                    user_tags.append("wanttoplay")
                if item.get("status").get("@wanttobuy") == "1":
                    user_tags.append("wanttobuy")
                if item.get("status").get("@wishlist") == "1":
                    user_tags.append("wishlist")
                if item.get("status").get("@preordered") == "1":
                    user_tags.append("preordered")
                if item.get("status").get("@own") == "0" and item.get("status").get("@prevowned") == "0" and item.get(
                        "status").get("@fortrade") == "0" and item.get("status").get("@want") == "0" and item.get(
                        "status").get("@wanttoplay") == "0" and item.get("status").get("@wanttobuy") == "0" and item.get(
                        "status").get("@wishlist") == "0" and item.get("status").get("@preordered") == "0":
                    user_tags.append("notag")
                if make_int(item.get("stats").get("rating").get("@value", None)) is None:
                    user_tags.append("norating")
                if item.get("comment", "") == "":
                    user_tags.append("nocomment")
                if make_int(item.get("numplays", None)) == 0:
                    user_tags.append("noplays")

                if game.get("type"):
                    user_tags.append(game.get("type"))

                if not any(x in user_tags for x in paramenters):
                    total_items += 1
                    collection[item["@objectid"]] = {
                        "type": game.get("type"),
                        "title": game.get("title"),
                        "yearpublished": item.get("yearpublished", ""),
                        "thumbnail": game.get("thumbnail"),
                        "dominant_colors": game.get("dominant_colors") or ["#3f3a60", "#3f3a60"],
                        "stats": {
                            "minplayers": make_int(game.get("stats").get("minplayers", None)),
                            "maxplayers": make_int(game.get("stats").get("maxplayers", None)),
                            "minplaytime": make_int(game.get("stats").get("minplaytime", None)),
                            "maxplaytime": make_int(game.get("stats").get("maxplaytime", None)),
                            "numowned": make_int(game.get("stats").get("numowned", None)),
                            "numcomments": make_int(game.get("stats").get("numcomments", None)),
                            "numweights": make_int(game.get("stats").get("numweights", None)),
                            "averageweight": make_float(game.get("stats").get("averageweight", None), 2),
                            "numrating": make_int(game.get("stats").get("numrating", None)),
                            "average": make_float(game.get("stats").get("average", None)),
                            "bayesaverage": make_float(game.get("stats").get("bayesaverage", None)),
                        },
                        "users": {
                            username: {
                                "rating": make_float(item.get("stats").get("rating").get("@value", None)),
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
                                    "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0),
                                                                      '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
                                }
                            }
                        },
                        "user": {
                            "rating": make_float(item.get("stats").get("rating").get("@value", None)),
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
                    if make_int(item.get("stats").get("rating").get("@value", None)):
                        match_items_rating += 1
                    if item.get("comment"):
                        match_items_comment += 1
            loading_status.append({
                "username": username,
                "status": 1,
                "updated_at": datetime.strftime(result["message"]["updated_at"], "%Y-%m-%d"),
                "total_items": total_items,
                "match_items": total_items,
                "total_items_rating": match_items_rating,
                "match_items_rating": match_items_rating,
                "total_items_comment": match_items_comment,
                "match_items_comment": match_items_comment,
                "mean_diff_rating": -100,
            })
        except AttributeError:
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
            total_items_rating = 0
            match_items_rating = 0
            total_items_comment = 0
            match_items_comment = 0
            if make_int(result["collection"].get("items").get("@totalitems")) > 0:
                if make_int(result["collection"].get("items").get("@totalitems")) == 1:
                    result["collection"]["items"]["item"] = [result["collection"].get("items").get("item")]
                for item in result["collection"].get("items").get("item"):
                    total_items += 1
                    if make_int(item.get("stats").get("rating").get("@value", None)):
                        total_items_rating += 1
                    if item.get("comment"):
                        total_items_comment += 1
                    if item["@objectid"] in collection.keys():
                        match_items += 1
                        diff_rating = make_float(calc_diff(make_float(item.get("stats").get("rating").get("@value", None)),
                                                collection[item["@objectid"]]["user"]["rating"]))
                        collection[item["@objectid"]]["users"][username] = {
                            "rating": make_float(item.get("stats").get("rating").get("@value", None)),
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
                                "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0),
                                                                  '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
                            }
                        }
                        if make_int(item.get("stats").get("rating").get("@value", None)):
                            match_items_rating += 1
                        if item.get("comment"):
                            match_items_comment += 1
                        if isinstance(diff_rating, float) and diff_rating >= 0:
                            title = get_title(item.get("originalname", ""), item.get("name").get("#text", ""), "title")
                            diff_ratings.append({"title": title, "diff_rating": diff_rating})

            loading_status.append({
                "username": username,
                "status": 1,
                "updated_at": datetime.strftime(result["message"]["updated_at"], "%Y-%m-%d"),
                "mean_diff_rating": make_float(statistics.mean([i["diff_rating"] for i in diff_ratings])) if len(
                    diff_ratings) > 0 else None,
                "diff_ratings": sorted(diff_ratings, key=lambda item: item["diff_rating"]),
                "total_items": total_items,
                "match_items": match_items,
                "total_items_rating": total_items_rating,
                "match_items_rating": match_items_rating,
                "total_items_comment": total_items_comment,
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
        count_comments = 0
        count_ratings = 0
        count_users = 0
        for _, user in item["users"].items():
            if make_int(user["rating"]) in range(1, 11):
                ratings.append(user["rating"])
                count_ratings += 1
            if isinstance(user["diff_rating"], float) and user["diff_rating"] >= 0:
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

            parameters = list()
            for user in user_list:
                parameters.append((user, "add_user"))
            user_status["collection_url"] = build_url(parameters)

            # remove user from list
            remove_list = [u["username"] for u in loading_status]
            remove_list.pop(remove_list.index(user_status["username"]))
            parameters = list()
            for user in remove_list:
                parameters.append((user, "add_user"))
            user_status["remove_collection_url"] = build_url(parameters)
        return loading_status
    elif loading_status:
        loading_status[0]["collection_url"] = None
        loading_status[0]["remove_collection_url"] = None
    return loading_status
