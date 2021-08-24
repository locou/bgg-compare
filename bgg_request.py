import re
import urllib.request
import json
import xmltodict


def request_collection(username):
    username = re.sub("[^a-zA-Z0-9 ]", "_", username)
    with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/collection?stats=1&username=" +
                                username.replace(" ", "%20")) as response:
        return xmltodict.parse(response.read())


def handle_collection_request(username):
    message = {"username": username, "status": 0, "message": "Unknown error"}
    try:
        request = request_collection(username)
        if "items" in request:
            message = {"username": username, "status": 1}
        elif "message" in request:
            message = {"username": username, "status": 0, "message": request.get("message", "")}
        else:
            try:
                message = {"username": username, "status": 0, "errors": request.get("errors").get("error").get("message")}
            except:
                message = {"username": username, "status": 0, "message": "API error"}
        return {"username": username, "result": json.dumps(request), "message": message}
    except:
        return {"username": username, "message": message}