import re
import urllib.request
import json
import xmltodict


def request_user_collection(username):
    username = re.sub("[^a-zA-Z0-9 ]", "_", username)
    message = {"username": username, "status": 0, "message": "Unknown error"}
    try:
        with urllib.request.urlopen("https://api.geekdo.com/xmlapi2/collection?stats=1&username=" +
                                    username.replace(" ", "%20")) as response:
            xml = response.read()
        result = xmltodict.parse(xml)
        if "items" in result:
            message = {"username": username, "status": 1}
        elif "message" in result:
            message = {"username": username, "status": 0, "message": result.get("message", "")}
        else:
            try:
                message = {"username": username, "status": 0, "errors": result.get("errors").get("error").get("message")}
            except:
                message = {"username": username, "status": 0, "message": "API error"}
        return {"username": username, "result": json.dumps(result), "message": message}
    except:
        return {"username": username, "message": message}