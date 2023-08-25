from vk_api import VkUpload, VkApi


class Photo:
    def __init__(self):
        self.upload: VkUpload = None
        self.path: str = None
        self.name: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path
    
    def send(self) -> str:
        photo = self.upload.photo_messages(self.path)[0]
        return f"photo{photo['owner_id']}_{photo['id']}"

    def prepare_to_download(self, name: str):
        self.name = name

    def download(self):
        path = ""
        return path

    def __str__(self):
        return self.name