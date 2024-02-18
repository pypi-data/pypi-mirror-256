from enum import Enum

from .client import NotionAPIClient, MediumAPIClient
from .render import NotionRender
from .callbacks import post_image_to_Medium, download_image


class PublishStatus(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class Converter:
    def __init__(self, src_api_key: str, tgt_api_key: str):
        self.src_api_key = src_api_key
        self.tgt_api_key = tgt_api_key
        self.src_api_client = NotionAPIClient(self.src_api_key)
        self.tgt_api_client = MediumAPIClient(self.tgt_api_key)
        self.render = NotionRender(
            callbacks=[
                download_image,
                lambda block: post_image_to_Medium(block, self.tgt_api_client),
            ]
        )

    def pull_and_post(self, src_doc_id: str, publishStatus: PublishStatus) -> dict:
        if self.src_api_client is None or self.tgt_api_client is None:
            raise
        page = self.src_api_client.get_page(src_doc_id, recursive=True)
        article = self.render.render(page)
        article["contentFormat"] = "html"
        article["publishStatus"] = publishStatus
        print(article["content"])
        return self.tgt_api_client.post_article(article)

    def __enter__(self):
        self.src_api_client.__enter__()
        self.tgt_api_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.src_api_client.__exit__(exc_type, exc_value, traceback)
        self.tgt_api_client.__exit__(exc_type, exc_value, traceback)
