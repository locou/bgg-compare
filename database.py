import os
import uuid
import json
# import cv2
import psycopg2
from datetime import datetime, timedelta
from bottle_postgresql import Configuration, Database
from psycopg2.extras import execute_values

from bgg_request import handle_collection_request, request_games
from dotenv import load_dotenv
# from skimage import io
# from sklearn.cluster import MiniBatchKMeans

load_dotenv()

configuration_dict = {
    "database": os.environ.get("DATABASE_NAME", ""),
    "host": os.environ.get("DATABASE_HOST", ""),
    "max_connection": os.environ.get("DATABASE_MAX_CONNECTION", 0),
    "password": os.environ.get("DATABASE_PASSWORD", ""),
    "port": os.environ.get("DATABASE_PORT", 0),
    "print_sql": os.environ.get("DATABASE_PRINT_SQL", True),
    "username": os.environ.get("DATABASE_USERNAME", "")
}


def calc_item_totals(result):
    total_items = 0
    total_ratings = 0
    total_comments = 0
    try:
        total_items = int(json.loads(result["result"])["items"]["@totalitems"])
        if total_items:
            total_ratings = sum(map(lambda item: item.get("stats").get("rating").get("@value", "N/A") != "N/A",
                                    json.loads(result["result"])["items"]["item"]))
            total_comments = sum(
                map(lambda item: item.get("comment", None) is not None, json.loads(result["result"])["items"]["item"]))
    except AttributeError as err:
        print(err)
    except KeyError as err:
        print(err)

    return total_items, total_ratings, total_comments


def calc_cluster(img):
    return None

# def calc_cluster(img):
#     def rgb2hex(r, g, b):
#         return "#{:02x}{:02x}{:02x}".format(r, g, b)
#     image = io.imread(img)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = cv2.resize(image, (15, 15))
#     reshape = image.reshape((image.shape[0] * image.shape[1], 3))
#
#     cluster = MiniBatchKMeans(n_clusters=2).fit(reshape)
#     rgb_cluster = [rgb2hex(int(r), int(g), int(b)) for b, g, r in cluster.cluster_centers_]
#     return rgb_cluster


def connect():
    configuration = Configuration(configuration_dict=configuration_dict)
    return Database(configuration)


def connect_psy():
    return psycopg2.connect("dbname=" + os.environ.get("DATABASE_NAME", "") +
                            " user=" + os.environ.get("DATABASE_USERNAME", "") +
                            " password=" + os.environ.get("DATABASE_PASSWORD", "") +
                            " port=" + os.environ.get("DATABASE_PORT", 0) +
                            " host=" + os.environ.get("DATABASE_HOST", ""))


def refresh_collection_cache(username):
    with connect() as connection:
        (
            connection
            .execute("UPDATE \"bgg-compare\".user_collection "
                     "SET updated_at = %(updated_at)s "
                     "WHERE LOWER(username) = LOWER(%(username)s)",
                     {"username": username, "updated_at": None})
        )


def select_collection(username):
    with connect() as connection:
        return (
            connection
            .execute("SELECT * FROM \"bgg-compare\".user_collection WHERE LOWER(username) = LOWER(%(username)s);",
                     {"username": username})
            .fetch_one()
        )


def update_collection(username, result):
    total_items, total_ratings, total_comments = calc_item_totals(result)

    with connect() as connection:
        (
            connection
            .execute("UPDATE \"bgg-compare\".user_collection "
                     "SET "
                     "updated_at = %(updated_at)s, "
                     "collection = %(collection)s, "
                     "total_items = %(total_items)s, "
                     "total_ratings = %(total_ratings)s, "
                     "total_comments = %(total_comments)s "
                     "WHERE LOWER(username) = LOWER(%(username)s)",
                     {"username": username,
                      "updated_at": datetime.now(),
                      "collection": result["result"],
                      "total_items": total_items,
                      "total_ratings": total_ratings,
                      "total_comments": total_comments,
                      }
                     )
        )
        return total_items, total_ratings, total_comments


def select_games(game_ids):
    if len(game_ids) > 0:
        conn = connect_psy()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"bgg-compare\".games WHERE game_id IN %(game_ids)s;",
                            {"game_ids": game_ids, "cache_date": datetime.now() - timedelta(days=31)})
                games_found = cur.fetchall()
        conn.close()
        return games_found
    else:
        return []


def insert_and_select_games(game_ids, parameter_values):
    conn = connect_psy()
    with conn:
        with conn.cursor() as cur:
            execute_values(cur, "INSERT INTO \"bgg-compare\".games ("
                                "uuid, "
                                "game_id, "
                                "title, "
                                "thumbnail, "
                                "type, "
                                "json) VALUES %s "
                                "ON CONFLICT (game_id) DO UPDATE SET "
                                "title = EXCLUDED.title,"
                                "thumbnail = EXCLUDED.thumbnail,"
                                "type = EXCLUDED.type,"
                                "json = EXCLUDED.json,"
                                "updated_at = current_timestamp;", parameter_values)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM \"bgg-compare\".games WHERE game_id IN %(game_ids)s;", {"game_ids": game_ids})
            games_found = cur.fetchall()

    conn.close()
    return games_found


def update_game_colours(parameter_values):
    conn = connect_psy()
    with conn:
        with conn.cursor() as cur:
            execute_values(cur, "UPDATE \"bgg-compare\".games AS g "
                                "SET dominant_colors = v.dominant_colours "
                                "FROM (VALUES %s) AS v(game_id, dominant_colours) "
                                "WHERE g.game_id = v.game_id;", parameter_values)
    conn.close()


def get_or_create_games(collection_game_ids):
    # CREATE UNIQUE INDEX index_game_id ON  "bgg-compare".games(game_id);

    games_found = select_games(tuple(collection_game_ids))
    print(str(len(games_found)) + " games requested")
    game_ids_found = [int(g[1]) for g in games_found]
    game_ids_not_found = list(set(collection_game_ids) ^ set(game_ids_found))

    print(str(len(game_ids_not_found))+" games not found")

    parameter_values = list()
    game_ids_not_found_chunks = [game_ids_not_found[x:x + 100] for x in range(0, len(game_ids_not_found), 100)]
    for game_ids in game_ids_not_found_chunks:

        games = request_games(game_ids)
        if games and games["items"].get("item"):
            if isinstance(games["items"]["item"], dict):
                games["items"]["item"] = [games["items"]["item"]]
            for game in games["items"]["item"]:
                if isinstance(game["name"], list):
                    title = game["name"][0]["@value"]
                else:
                    title = game["name"]["@value"]
                parameter_values.append(
                    (
                        str(uuid.uuid4()),
                        int(game["@id"]),
                        str(title),
                        str(game.get("thumbnail", None)),
                        str(game["@type"]),
                        json.dumps(game)
                    )
                )

    if game_ids_not_found and len(parameter_values) > 0:
        games_found = insert_and_select_games(tuple(collection_game_ids), parameter_values)
    else:
        games_found = select_games(tuple(collection_game_ids))
    games_data = dict()
    i = 0
    update_colors_values = list()
    for game in games_found:
        if i < 25 and game[5] is None and game[3] is not None and game[3] != "None":
            i += 1
            print(str(i)+" calc_cluster "+str(game[2]) + " - " + str(game[3]))
            dominant_colours = calc_cluster(game[3])
            update_colors_values.append((game[1], dominant_colours))
        else:
            dominant_colours = None

        averageweight = game[6]["statistics"]["ratings"]["averageweight"]["@value"]
        if float(averageweight) < 1:
            averageweight = None

        games_data[game[1]] = {"title": game[2],
                               "thumbnail": game[3],
                               "type": game[4],
                               "dominant_colors": dominant_colours or game[5],
                               "stats": {
                                   "minplayers": game[6]["minplayers"]["@value"],
                                   "maxplayers": game[6]["maxplayers"]["@value"],
                                   "minplaytime": game[6]["minplaytime"]["@value"],
                                   "maxplaytime": game[6]["maxplaytime"]["@value"],
                                   "numowned": game[6]["statistics"]["ratings"]["owned"]["@value"],
                                   "numcomments": game[6]["statistics"]["ratings"]["numcomments"][
                                       "@value"],
                                   "numweights": game[6]["statistics"]["ratings"]["numweights"]["@value"],
                                   "averageweight": averageweight,
                                   "numrating": game[6]["statistics"]["ratings"]["usersrated"]["@value"],
                                   "average": game[6]["statistics"]["ratings"]["average"]["@value"],
                                   "bayesaverage": game[6]["statistics"]["ratings"]["bayesaverage"][
                                       "@value"],
                               },
                               }
    # update_game_colours(update_colors_values)
    return games_data


def insert_collection(username, result):
    total_items, total_ratings, total_comments = calc_item_totals(result)
    with connect() as connection:
        return (
            connection
            .insert('"bgg-compare".user_collection')
            .set("id", str(uuid.uuid4()))
            .set("username", username)
            .set("collection", result["result"])
            .set("created_at", datetime.now())
            .set("updated_at", datetime.now())
            .set("total_items", total_items)
            .set("total_ratings", total_ratings)
            .set("total_comments", total_comments)
            .execute()
            .fetch_one()
        )


def get_or_create_collection(username):
    query_result = select_collection(username)
    if query_result:
        # TODO: limit how many collections can be requested at the same time.
        #  ex: if 4 of 10 users are cached, but outdated, don't update them
        if query_result.updated_at is None or divmod((datetime.now() - query_result.updated_at).total_seconds(), 3600)[0] > int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS", 0)):
            result = handle_collection_request(username)
            if result["message"]["status"] == 1:
                total_items, total_ratings, total_comments = update_collection(username, result)
                result["collection"] = json.loads(result["result"])
                result["message"]["updated_at"] = datetime.now()
                result["message"]["total_items"] = total_items
                result["message"]["total_ratings"] = total_ratings
                result["message"]["total_comments"] = total_comments
        else:
            result = {"username": username,
                      "message": {"username": username,
                                  "status": 1,
                                  "updated_at": query_result.updated_at,
                                  "total_items": query_result.total_items,
                                  "total_ratings": query_result.total_ratings,
                                  "total_comments": query_result.total_comments},
                      "collection": query_result.collection}
    else:
        result = handle_collection_request(username)
        if result["message"]["status"] == 1:
            query_result = insert_collection(username, result)
            result["collection"] = query_result.collection
            result["message"]["updated_at"] = datetime.now()
            result["message"]["total_items"] = query_result.total_items
            result["message"]["total_ratings"] = query_result.total_ratings
            result["message"]["total_comments"] = query_result.total_comments

    return result


def get_cached_usernames(exclude_usernames=[""]):
    try:
        exclude_usernames = [username.lower() for username in exclude_usernames]
        with connect() as connection:
            query_result = (
                connection
                .execute("SELECT "
                         "username, "
                         "to_char(created_at, 'YYYY-MM-DD') as created_at, "
                         "to_char(updated_at, 'YYYY-MM-DD') as updated_at, "
                         "total_items, "
                         "total_ratings, "
                         "total_comments "
                         "FROM \"bgg-compare\".user_collection "
                         "WHERE LOWER(username) NOT IN %(exclude_usernames)s "
                         "ORDER BY updated_at DESC;",
                         {"exclude_usernames": tuple(exclude_usernames)})
                .fetch_all()
            )
            return query_result
    except:
        return []
