from app.repository._Conn import Conn

class Encode:
    def __init__(self, data):
        self.data = data.get("data", None)
        self.conn = Conn()

    def action(self):
        password = self.data.get("password", None)

        data = {
            "response": "teste demais"
        }

        return data