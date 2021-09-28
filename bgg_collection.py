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


def item_status_into_list(item_status):
    user_tags = dict()
    if item_status.get("@own") == "1":
        user_tags["own"] = ("own", None)
    if item_status.get("@prevowned") == "1":
        user_tags["prevowned"] = ("prev. owned", "Previously owned this game")
    if item_status.get("@fortrade") == "1":
        user_tags["fortrade"] = ("for trade", None)
    if item_status.get("@want") == "1":
        user_tags["want"] = ("want", None)
    if item_status.get("@wanttoplay") == "1":
        user_tags["wanttoplay"] = ("want to play", None)
    if item_status.get("@wanttobuy") == "1":
        user_tags["wanttobuy"] = ("want to buy", None)
    if item_status.get("@wishlist") == "1":
        prio = item_status.get("@wishlistpriority", 0)
        if prio == "1":
            wishlist_txt = "Must have"
        elif prio == "2":
            wishlist_txt = "Love to have"
        elif prio == "3":
            wishlist_txt = "Like to have"
        elif prio == "4":
            wishlist_txt = "Thinking about it"
        elif prio == "5":
            wishlist_txt = "Don't buy this"
        else:
            wishlist_txt = ""

        user_tags["wishlist" + str(prio)] = ("wishlist " + str(prio), wishlist_txt)
    if item_status.get("@preordered") == "1":
        user_tags["preordered"] = "preordered"
    if item_status.get("@own") == "0" and \
            item_status.get("@prevowned") == "0" and \
            item_status.get("@fortrade") == "0" and \
            item_status.get("@want") == "0" and \
            item_status.get("@wanttoplay") == "0" and \
            item_status.get("@wanttobuy") == "0" and \
            item_status.get("@wishlist") == "0" and \
            item_status.get("@preordered") == "0":
        user_tags["notag"] = ("notag", None)
    return user_tags


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
            "total_items_rating": 0,
            "match_items_rating": 0,
            "total_items_comment": 0,
            "match_items_comment": 0,
            "mean_diff_rating": -100,
        })
    elif result["message"]["status"] == 1 and "item" in result["collection"]["items"]:
        try:
            if isinstance(result["collection"].get("items").get("item"), dict):
                result["collection"]["items"]["item"] = [result["collection"].get("items").get("item")]
            game_ids = list()
            user_tags = dict()
            item_tags = dict()
            for item in result["collection"].get("items").get("item"):
                item_id = int(item["@objectid"])
                user_tags[item_id] = item_status_into_list(item.get("status"))
                item_tags[item_id] = list(user_tags[item_id].keys())

                if make_int(item.get("stats").get("rating").get("@value", None)) is None:
                    item_tags[item_id].append("norating")
                if item.get("comment", "") == "":
                    item_tags[item_id].append("nocomment")
                if make_int(item.get("numplays", 0)) == 0:
                    item_tags[item_id].append("noplays")
                if not any(x in item_tags[item_id] for x in paramenters):
                    game_ids.append(item_id)
            games = get_or_create_games(game_ids)
            match_items = 0
            match_items_rating = 0
            match_items_comment = 0
            for game_id, game in games.items():
                if game and game.get("type"):
                    item_tags[game_id].append(game.get("type"))

                if game and not any(x in item_tags[game_id] for x in paramenters):
                    item = next(item for item in result["collection"].get("items").get("item") if int(item["@objectid"]) == game_id)
                    match_items += 1

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
                                "tags": user_tags[game_id],
                                "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0),
                                                                      '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
                            }
                        },
                        "user": {
                            "rating": make_float(item.get("stats").get("rating").get("@value", None)),
                            "numplays": make_int(item.get("numplays", None)),
                            "comment": item.get("comment", ""),
                            "tags": user_tags[game_id],
                            "lastmodified": item.get("status").get("@lastmodified", 0),
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
                "total_items": make_int(result["message"]["total_items"]),
                "match_items": match_items,
                "total_items_rating": make_int(result["message"]["total_ratings"]),
                "match_items_rating": match_items_rating,
                "total_items_comment": make_int(result["message"]["total_comments"]),
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
            match_items = 0
            match_items_rating = 0
            match_items_comment = 0
            if make_int(result["collection"].get("items").get("@totalitems")) > 0:
                if make_int(result["collection"].get("items").get("@totalitems")) == 1:
                    result["collection"]["items"]["item"] = [result["collection"].get("items").get("item")]
                for item in result["collection"].get("items").get("item"):
                    user_tags = item_status_into_list(item.get("status"))

                    if item["@objectid"] in collection.keys():
                        match_items += 1
                        diff_rating = make_float(calc_diff(make_float(item.get("stats").get("rating").get("@value", None)),
                                                collection[item["@objectid"]]["user"]["rating"]))
                        collection[item["@objectid"]]["users"][username] = {
                            "rating": make_float(item.get("stats").get("rating").get("@value", None)),
                            "diff_rating": diff_rating,
                            "numplays": make_int(item.get("numplays", None)),
                            "comment": item.get("comment", ""),
                            "tags": user_tags,
                            "lastmodified": datetime.strptime(item.get("status").get("@lastmodified", 0),
                                                              '%Y-%m-%d %H:%M:%S').strftime("%b %Y"),
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
                "total_items": make_int(result["message"]["total_items"]),
                "match_items": match_items,
                "total_items_rating": make_int(result["message"]["total_ratings"]),
                "match_items_rating": match_items_rating,
                "total_items_comment": make_int(result["message"]["total_comments"]),
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


def build_collection_url(loading_status, exclude_tags=[]):
    if len(loading_status) > 1:
        tag_parameters = []
        for exclude_tag in exclude_tags:
            tag_parameters.append((exclude_tag, "exclude"))
        for key, user_status in enumerate(loading_status):
            # move the user to the front of the list
            user_list = [u["username"] for u in loading_status]
            user_list.insert(0, user_list.pop(user_list.index(user_status["username"])))

            user_parameters = list()
            for user in user_list:
                user_parameters.append((user, "add_user"))
            user_status["collection_url"] = build_url(user_parameters+tag_parameters)

            # remove user from list
            remove_list = [u["username"] for u in loading_status]
            remove_list.pop(remove_list.index(user_status["username"]))
            user_parameters = list()
            for user in remove_list:
                user_parameters.append((user, "add_user"))
            user_status["remove_collection_url"] = build_url(user_parameters+tag_parameters)
        return loading_status
    elif loading_status:
        loading_status[0]["collection_url"] = None
        loading_status[0]["remove_collection_url"] = None
    return loading_status
