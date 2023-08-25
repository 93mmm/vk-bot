from vk_api import VkUpload, VkApi


class Doc:
    def __init__(self, ):
        self.upload: VkUpload = None
        self.path: str = None
        self.name: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path

    def send(self) -> str:
        doc = self.upload.document(self.path)["doc"]
        return f"doc{doc['owner_id']}_{doc['id']}"

    def prepare_to_download(self, name: str):
        self.name = name

    def download(self):
        path = ""
        return path

    def __str__(self):
        return self.name