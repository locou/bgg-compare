import os
import uuid
import json
from datetime import datetime
from bottle_postgresql import Configuration, Database
from bgg_request import handle_collection_request
from dotenv import load_dotenv

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


def connect():
    configuration = Configuration(configuration_dict=configuration_dict)
    return Database(configuration)


def select_collection(username):
    with connect() as connection:
        # TODO: make where conditions not case sensitive
        return (
            connection
                .select('"bgg-compare".user_collection')
                .where("username", username)
                .execute()
                .fetch_one()
        )


def update_collection(username, result):
    with connect() as connection:
        (
            connection
                .update('"bgg-compare".user_collection')
                .where("username", username)
                .set("updated_at", datetime.now())
                .set("collection", result["result"])
                .execute()
        )


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
        if divmod((datetime.now() - query_result.updated_at).total_seconds(), 3600)[0] > int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS", 0)):
            result = handle_collection_request(username)
            if result["message"]["status"] == 1:
                update_collection(username, result)
                result["collection"] = json.loads(result["result"])
        else:
            result = {"username": username, "message": {"username": username, "status": 1}, "collection": query_result.collection}
    else:
        result = handle_collection_request(username)
        if result["message"]["status"] == 1:
            query_result = insert_collection(username, result)
            result["collection"] = query_result.collection

    return result


def get_cached_usernames():
    try:
        with connect() as connection:
            query_result = (
                connection
                    .select('"bgg-compare".user_collection')
                    .fields('username', 'created_at', 'updated_at')
                    .order_by("updated_at")
                    .execute()
                    .fetch_all()
            )
            return query_result
    except:
        return
