from random import randint


class TextMessage:
    def __init__(self, peer_id, attachments, text="", sticker_id=0):
        self.peer_id = peer_id
        self.attachments = attachments
        self.text = text
        self.sticker_id = sticker_id
    
    def send(self, api):
        api.messages.send(peer_id=self.peer_id, 
                          random_id=randint(0, 100000),
                          message=self.text, 
                          attachment=",".join(list(map(str, self.attachments))),
                          sticker_id=self.sticker_id)
