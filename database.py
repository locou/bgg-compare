import os
import uuid
import json
import cv2
from datetime import datetime, timedelta
from bottle_postgresql import Configuration, Database
from bgg_request import handle_collection_request
from dotenv import load_dotenv
from skimage import io
from sklearn.cluster import MiniBatchKMeans

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


def calc_cluster(img):
    def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    image = io.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (15, 15))
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))

    cluster = MiniBatchKMeans(n_clusters=2).fit(reshape)
    rgb_cluster = [rgb2hex(int(r), int(g), int(b)) for b, g, r in cluster.cluster_centers_]
    return rgb_cluster


def connect():
    configuration = Configuration(configuration_dict=configuration_dict)
    return Database(configuration)


def refresh_collection_cache(username):
    with connect() as connection:
        (
            # TODO: set up database to accept Null in updated at
            connection
            .execute("UPDATE \"bgg-compare\".user_collection "
                     "SET updated_at = %(updated_at)s "
                     "WHERE LOWER(username) = LOWER(%(username)s)",
                     {"username": username, "updated_at": datetime.now() - timedelta(days=31)}
                     )
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
    with connect() as connection:
        (
            connection
            .execute("UPDATE \"bgg-compare\".user_collection "
                     "SET updated_at = %(updated_at)s, collection = %(collection)s "
                     "WHERE LOWER(username) = LOWER(%(username)s)",
                     {"username": username, "updated_at": datetime.now(), "collection": result["result"]}
                     )
        )


def get_or_create_games_color(games):
    # TODO: fetch & save (?) games with https://api.geekdo.com/xmlapi2/thing?id=174388 / subtype and categorys are there
    # TODO: calc color based on that preview image
    # TODO: collections with many games would do that many api calls as well (worth it?) (cache for a week?)
    with connect() as connection:
        (
            connection
            .execute("CREATE TABLE IF NOT EXISTS \"bgg-compare\".game_color"
                     "(game_id integer PRIMARY KEY,"
                     "colors varchar(40)[])")
        )
    with connect() as connection:
        games_found = (
            connection
            .execute("SELECT * FROM \"bgg-compare\".game_color WHERE game_id IN %(game_ids)s;",
                     {"game_ids": tuple(games.keys())})
            .fetch_all()
        )

    game_ids_found = [str(g.game_id) for g in games_found]
    game_ids_not_found = set(games.keys()) ^ set(game_ids_found)

    values = list()
    i = 0
    print(str(len(game_ids_not_found))+" games not found")
    for game_id in game_ids_not_found:
        i+=1
        if i <= 10 and games[game_id]:
            print(str(i)+": "+games[game_id])
            values.append((int(game_id), tuple(calc_cluster(games[game_id]))))
    parameters = "("+"),(".join([str(game)+", '{"+",".join(color)+"}'" for game, color in values])+")"

    if game_ids_not_found:
        with connect() as connection:
            (
                connection
                .execute("INSERT INTO \"bgg-compare\".game_color (game_id, colors)"
                         "(VALUES "+parameters+")"
                         "ON CONFLICT (game_id) DO NOTHING;")
            )
            games_found = (
                connection
                .execute("SELECT * FROM \"bgg-compare\".game_color WHERE game_id IN %(game_ids)s;",
                         {"game_ids": tuple(games.keys())})
                .fetch_all()
            )
    else:
        with connect() as connection:
            games_found = (
                connection
                .execute("SELECT * FROM \"bgg-compare\".game_color WHERE game_id IN %(game_ids)s;",
                         {"game_ids": tuple(games.keys())})
                .fetch_all()
            )
    games_color = dict()
    for game in games_found:
        games_color[game.game_id] = game.colors
    return games_color


def insert_collection(username, result):
    with connect() as connection:
        return (
            connection
            .insert('"bgg-compare".user_collection')
            .set("id", str(uuid.uuid4()))
            .set("username", username)
            .set("collection", result["result"])
            .set("created_at", datetime.now())
            .set("updated_at", datetime.now())
            .execute()
            .fetch_one()
        )


def get_or_create_collection(username):
    query_result = select_collection(username)
    if query_result:
        # TODO: limit how many collections can be requested at the same time.
        #  ex: if 4 of 10 users are cached, but outdated, don't update them
        if divmod((datetime.now() - query_result.updated_at).total_seconds(), 3600)[0] > int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS", 0)):
            result = handle_collection_request(username)
            if result["message"]["status"] == 1:
                update_collection(username, result)
                result["collection"] = json.loads(result["result"])
                result["message"]["updated_at"] = datetime.now()
        else:
            result = {"username": username,
                      "message": {"username": username, "status": 1, "updated_at": query_result.updated_at},
                      "collection": query_result.collection}
    else:
        result = handle_collection_request(username)
        if result["message"]["status"] == 1:
            query_result = insert_collection(username, result)
            result["collection"] = query_result.collection
            result["message"]["updated_at"] = datetime.now()

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
                         "to_char(updated_at, 'YYYY-MM-DD') as updated_at "
                         "FROM \"bgg-compare\".user_collection "
                         "WHERE LOWER(username) NOT IN %(exclude_usernames)s "
                         "ORDER BY updated_at DESC;",
                         {"exclude_usernames": tuple(exclude_usernames)})
                .fetch_all()
            )
            return query_result
    except:
        return []
