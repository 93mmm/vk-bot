from requests import get

def get_photo_url(sizes: list[dict]) -> str:
    # I've read the documentation, so it's better to search this way
    max_h, idx = sizes[0]["height"], 0
    for index, sz in enumerate(sizes):
        if sizes[index]["height"] > max_h:
            max_h, idx = sizes[idx]["height"], index
    return sizes[idx]["url"]


def download_and_save(path: str, url: str):
    with open(path, "wb") as file:
        file.write(get(url).content)