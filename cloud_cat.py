from websocket import create_connection
import json
import random
import string


class CloudCat(object):
    def __init__(self, salt):
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        random.seed(salt)
        self._reader_id = "".join(random.sample(chars, 16))
        self._writer_id = "".join(random.sample(chars, 16))

    def read(self):
        ws = self._connect(self._reader_id)

        try:
            while True:
                message = json.loads(ws.recv())

                if message["FROM"] == self._writer_id:
                    text = message["payload"]
                    return text
        finally:
            ws.close()

    def write(self, text):
        ws = self._connect(self._writer_id)

        try:
            message = json.dumps({
                "to": self._reader_id,
                "payload": text,
            })

            ws.send(message)
        finally:
            ws.close()

    @staticmethod
    def _connect(id_):
        ws = create_connection("ws://achex.ca:4010")
        ws.recv()

        auth = json.dumps({
            "setID": id_,
            "passwd": "NONE",
        })

        ws.send(auth)
        message = json.loads(ws.recv())
        assert(message["auth"] == "ok")
        return ws
