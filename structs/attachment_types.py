from time import sleep
from vk_api import VkUpload


class Voice:
    def __init__(self, vk, path):
        self.vk = vk
        self.api = vk.get_api()
        self.path = path

    def __str__(self):
        sleep(0.2)
        upload = VkUpload(self.vk)
        voice = upload.audio_message(self.path)["audio_message"]
        return f"audio_message{voice['owner_id']}_{voice['id']}"


class Doc:
    def __init__(self, vk, path):
        self.vk = vk
        self.api = vk.get_api()
        self.path = path

    def __str__(self):
        sleep(0.2)
        upload = VkUpload(self.vk)
        doc = upload.document(self.path)["doc"]
        return f"doc{doc['owner_id']}_{doc['id']}"
        

class Photo:
    def __init__(self, vk, path):
        self.vk = vk
        self.api = vk.get_api
        self.path = path
    
    def __str__(self):
        sleep(0.2)
        upload = VkUpload(self.vk)
        photo = upload.photo_messages(self.path)[0]
        return f"photo{photo['owner_id']}_{photo['id']}"