import os
import random
import re
import urllib.request
import json
import socket
import time
import xmltodict


def request_collection(username):
    username = re.sub("[^a-zA-Z0-9-_ ]", "_", username)
    try:
        with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/collection?stats=1&username=" +
                                    username.replace(" ", "%20"), timeout=10) as response:
            return xmltodict.parse(response.read())
    except socket.timeout:
        print("connection's timeout expired")


def request_user(username):
    username = re.sub("[^a-zA-Z0-9-_ ]", "_", username)
    try:
        with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/user?buddies=1&name=" +
                                    username.replace(" ", "%20"), timeout=10) as response:
            return xmltodict.parse(response.read())
    except socket.timeout:
        print("connection's timeout expired")


def request_games(game_ids):
    try:
        with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/thing?stats=1&id=" + ",".join(str(x) for x in game_ids), timeout=10) as response:
            time.sleep(2)
            return xmltodict.parse(response.read())
    except socket.timeout:
        print("connection's timeout expired")


def handle_user_request(username):
    try:
        # TODO: request multiple pages for buddies
        user_data = request_user(username)
        buddies = [user["@name"] for user in user_data["user"]["buddies"]["buddy"] if len(user["@name"]) > 0]
        random.shuffle(buddies)
        return buddies
    except:
        return []


def handle_collection_request(username):
    message = {"username": username, "status": 0, "errors": "Unknown error"}
    try:
        request = request_collection(username)
        if "items" in request:
            message = {"username": username, "status": 1}
        elif "message" in request:
            api_message = request.get("message", "")
            if api_message == "Your request for this collection has been accepted and will be processed.  Please try again later for access.":
                api_message = "Collection was requested. Reload this page in a few seconds to show the result."
            message = {"username": username, "status": 0, "message": api_message}
        else:
            try:
                if "errors" in request:
                    message = {"username": username, "status": 0, "errors": request.get("errors").get("error").get("message")}
                if "error" in request:
                    message = {"username": username, "status": 0, "errors": request.get("error").get("message")}
            except:
                message = {"username": username, "status": 0, "message": "API error"}
        return {"username": username, "result": json.dumps(request), "message": message}
    except:
        return {"username": username, "message": message}
