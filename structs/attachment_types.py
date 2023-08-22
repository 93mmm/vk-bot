from time import sleep
from vk_api import VkUpload


class Voice:
    def __init__(self, vk, path):
        self.upload = VkUpload(vk)
        self.path = path

    def __str__(self):
        sleep(0.2)
        voice = self.upload.audio_message(self.path)["audio_message"]
        return f"audio_message{voice['owner_id']}_{voice['id']}"


class Doc:
    def __init__(self, vk, path):
        self.upload = VkUpload(vk)
        self.path = path

    def __str__(self):
        sleep(0.2)
        doc = self.upload.document(self.path)["doc"]
        return f"doc{doc['owner_id']}_{doc['id']}"
        

class Photo:
    def __init__(self, vk, path):
        self.upload = VkUpload(vk)
        self.path = path
    
    def __str__(self):
        sleep(0.2)
        photo = self.upload.photo_messages(self.path)[0]
        return f"photo{photo['owner_id']}_{photo['id']}"