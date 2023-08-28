from const import CONVERSATION_CACHES, NOT_FOUND
from helpers import read_json, write_json


class LinkCaches:
    def __init__(self):
        self._sent_docs: dict = None

        self._sent_docs = read_json(CONVERSATION_CACHES)

    def get_link(self, path: str) -> str:
        if path in self._sent_docs:
            print("got the link")
            return self._sent_docs[peer_id]
        return NOT_FOUND
    
    def add_link(self, key: str, value: str):
        self._sent_docs[key] = value
        write_json(self._sent_docs)


class ConversationCaches:
    def __init__(self):
        self._conversations: dict = None

        self._conversations = read_json(CONVERSATION_CACHES)

    def get_name(self, peer_id: int) -> str:
        peer_id = str(peer_id)
        if peer_id in self._conversations:
            return self._conversations[peer_id]
        return NOT_FOUND
    
    def add_conv(self, key: str, value: str):
        self._conversations[key] = value
        write_json(self._conversations)
