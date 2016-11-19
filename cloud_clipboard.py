import json
import requests
import sys
import time

import config


def help():
    print("{} <get|set>".format(sys.argv[0]))


def get_cloud_clipboard():
    session = requests.Session()
    auth = (config.PASTY_USER, config.PASTY_PASSWORD)

    while True:
        response = session.get(config.PASTY_API_ROOT_PATH + "clipboard/list.json", auth=auth)
        response.raise_for_status()
        data = json.loads(response.text)["payload"]
        items = data["items"]

        if len(items) == 0:
            time.sleep(config.PASTY_CLIPBOARD_REFRESH_INTERVAL)
        else:
            item = items[-1]
            item_id = item["_id"]
            response = session.get(config.PASTY_API_ROOT_PATH + "clipboard/item/" + item_id, auth=auth)
            response.raise_for_status()
            data = json.loads(response.text)["payload"]
            text = data["item"]
            response = session.delete(config.PASTY_API_ROOT_PATH + "clipboard/item/" + item_id, auth=auth)
            return text


def set_cloud_clipboard(text):
    auth = (config.PASTY_USER, config.PASTY_PASSWORD)
    data = {"item": text}
    response = requests.post(config.PASTY_API_ROOT_PATH + "clipboard/item/", auth=auth, json=data)
    response.raise_for_status()
    time.sleep(config.PASTY_CLIPBOARD_REFRESH_INTERVAL / 2)


def main():
    if len(sys.argv) != 2 or not sys.argv[1] in ("set", "get"):
        help()
        sys.exit(1)

    if sys.argv[1] == "get":
        text = get_cloud_clipboard()
        sys.stdout.write(text)
    elif sys.argv[1] == "set":
        text = sys.stdin.read()
        set_cloud_clipboard(text)
    else:
        assert(False)


if __name__ == "__main__":
    main()
