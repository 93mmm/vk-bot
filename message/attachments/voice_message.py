from vk_api import VkUpload, VkApi


class Voice:
    def __init__(self):
        self.upload: VkUpload = None
        self.path: str = None
        self.name: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path

    def send(self) -> str:
        voice = self.upload.audio_message(self.path)["audio_message"]
        return f"audio_message{voice['owner_id']}_{voice['id']}"

    def prepare_to_download(self, name: str):
        self.name = name

    def download(self):
        path = ""
        return path

    def __str__(self):
        return self.name