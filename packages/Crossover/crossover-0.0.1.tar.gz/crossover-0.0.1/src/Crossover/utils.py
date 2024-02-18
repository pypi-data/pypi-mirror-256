from urllib.parse import urlparse
from urllib.request import urlretrieve
import os
import json
import hashlib

from platformdirs import user_data_dir

from .__version__ import APP_NAME, AUTHOR


def is_local(url: str) -> bool:
    url_parsed = urlparse(url)
    if url_parsed.scheme in ("file", ""):  # Possibly a local file
        return os.path.exists(url_parsed.path)
    return False


def get_image_url_cache(img_path: str) -> str | None:
    # load cache
    cache_path = os.path.join(user_data_dir(APP_NAME, AUTHOR), "md52imgurl.json")
    if not os.path.exists(cache_path):
        return None
    with open(cache_path, "r") as h:
        md52imgurl = json.load(h)
    # get image md5
    md5 = get_md5(img_path)
    return md52imgurl.get(md5, None)


def save_image_url_cache(md5: str, url: str) -> None:
    # load cache
    cache_path = os.path.join(user_data_dir(APP_NAME, AUTHOR), "md52imgurl.json")
    if not os.path.exists(cache_path):
        md52imgurl = {}
    else:
        with open(cache_path, "r") as h:
            md52imgurl = json.load(h)
    # update cahce
    md52imgurl[md5] = url
    # save back
    with open(cache_path, "w") as h:
        json.dump(md52imgurl, h, indent=4)


def get_md5(fp: str) -> str:
    if not os.path.exists(fp):
        raise FileNotFoundError(fp)
    # Open the file in binary mode
    with open(fp, "rb") as h:
        # Read the contents of the file
        data = h.read()
        # Compute the MD5 hash
        md5_hash = hashlib.md5(data).hexdigest()
        return md5_hash


def download_to_temp_dir(url: str) -> tuple[str, dict]:
    img_name = url.split("?", 1)[0].rsplit("/", 1)[-1]
    dst_dir = user_data_dir(APP_NAME, AUTHOR)
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, img_name)
    dst_path, headers = urlretrieve(url, dst_path)
    return dst_path, headers
