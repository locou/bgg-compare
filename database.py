import os
import uuid
import json
from datetime import datetime
from bottle_postgresql import Configuration, Database
from request import request_user_collection
from dotenv import load_dotenv

load_dotenv()

configuration_dict = {
    "database": os.environ.get("DATABASE_NAME"),
    "host": os.environ.get("DATABASE_HOST"),
    "max_connection": os.environ.get("DATABASE_MAX_CONNECTION"),
    "password": os.environ.get("DATABASE_PASSWORD"),
    "port": os.environ.get("DATABASE_PORT"),
    "print_sql": os.environ.get("DATABASE_PRINT_SQL"),
    "username": os.environ.get("DATABASE_USERNAME")
}

configuration = Configuration(configuration_dict=configuration_dict)


def connect():
    return Database(configuration)


def get_or_create_collection(username):
    with connect() as connection:
        query_result = (
            connection
                .select('"bgg-compare".user_collection')
                .where("username", username)
                .execute()
                .fetch_one()
        )
    if query_result:
        if divmod((datetime.now() - query_result.updated_at).total_seconds(), 3600)[0] > int(os.environ.get("COLLECTION_CACHE_EXPIRE_HOURS")):
            result = request_user_collection(username)
            if result["message"]["status"] == 1:
                with connect() as connection:
                    (
                        connection
                            .update('"bgg-compare".user_collection')
                            .where("username", username)
                            .set("updated_at", datetime.now())
                            .set("collection", result["result"])
                            .execute()
                    )
                result["collection"] = json.loads(result["result"])
        else:
            result = {"username": username, "message": {"username": username, "status": 1}, "collection": query_result.collection}
    else:
        result = request_user_collection(username)
        if result["message"]["status"] == 1:
            with connect() as connection:
                query_result = (
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
            result["collection"] = query_result.collection

    return result