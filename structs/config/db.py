from helpers import read_json


DATABASE = "files/json/conversations.json"


class JsonDialogsDB:
    NOT_FOUND = "NF"
    def __init__(self):
        self.data: dict = None
        
        self.data = read_json(DATABASE)

    def get_name(self, peer_id: int) -> str:
        peer_id = str(peer_id)
        if peer_id in self.data:
            return self.data[peer_id]
        return self.NOT_FOUND
