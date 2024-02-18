import os

from .utils import (
    is_local,
    get_image_url_cache,
    save_image_url_cache,
    download_to_temp_dir,
)

from .client import MediumAPIClient


def post_image_to_Medium(block: dict, client: MediumAPIClient) -> None:
    if block["type"] == "image":
        img_path = block["image"]["file"]["url"]
        if is_local(img_path):
            # check for local cache
            url = get_image_url_cache(img_path)
            if url is None:
                res = client.post_image(img_path)
                url = res["data"]["url"]
                md5 = res["data"]["md5"]
                save_image_url_cache(md5, url)
                os.remove(img_path)
            block["image"]["file"]["url"] = url


def download_image(block: dict) -> None:
    """This function works on image blocks of Notion. Since Notion image URLs are dynamic, we need to download it and then optionally upload it somewhere else."""
    if block["type"] == "image":
        url = block["image"]["file"]["url"]
        img_path, headers = download_to_temp_dir(url)
        block["image"]["file"]["url"] = img_path
