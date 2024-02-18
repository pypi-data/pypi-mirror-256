import json
import http.client
import mimetypes
import os


class APIClient:
    def __init__(self, api_base: str, api_key: str):
        self.api_key = api_key
        self.api_base = api_base
        self.conn = None

    def get(self, end_point: str, parse: bool = True, **kwargs):
        self.conn.request("GET", end_point, **kwargs)
        res = self.conn.getresponse()
        self.handle_error(res)
        if parse:
            res = json.loads(res.read().decode())
        return res

    def post(self, end_point: str, parse: bool = True, **kwargs):
        self.conn.request("POST", end_point, **kwargs)
        res = self.conn.getresponse()
        self.handle_error(res)
        if parse:
            res = json.loads(res.read().decode())
        return res

    def handle_error(self, res):
        if res.status >= 400:
            print(res.status)
            print(res.reason)
            raise

    def connect(self):
        if self.conn is None:
            self.conn = http.client.HTTPSConnection(self.api_base)

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()


class NotionAPIClient(APIClient):
    API_BASE = "api.notion.com"

    def __init__(self, api_key):
        super().__init__(self.API_BASE, api_key)

    def get_page(self, page_id, recursive=False, parse=True):
        if recursive and not parse:
            raise "Must parse json to dict when recursive is true."
        res = self.get(f"/v1/blocks/{page_id}", headers=self.get_headers(), parse=parse)
        if recursive:
            children = self.get_children(page_id, recursive=recursive, parse=parse)
            res["children"] = children
        return res

    def get_children(self, page_id, parse=True, recursive=False):
        res = self.get(
            f"/v1/blocks/{page_id}/children", headers=self.get_headers(), parse=parse
        )
        if recursive:
            for child in res["results"]:
                if child["has_children"]:
                    children = self.get_children(
                        child["id"], parse=parse, recursive=recursive
                    )
                    child["children"] = children
        return res

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
        }


class MediumAPIClient(APIClient):
    API_BASE = "api.medium.com"

    def __init__(self, api_key: str):
        super().__init__(self.API_BASE, api_key)
        self.me = None

    def get_me(self, parse: bool = True):
        res = self.get("/v1/me", headers=self.get_headers(), parse=parse)
        return res

    def get_publications(self, parse: bool = True):
        res = self.get(
            f"/v1/users/{self.me['id']}/publications",
            headers=self.get_headers(),
            parse=parse,
        )
        return res

    def post_article(self, article: dict, parse: bool = True):
        res = self.post(
            f"/v1/users/{self.me['id']}/posts",
            body=json.dumps(article),
            headers=self.get_headers(),
            parse=parse,
        )
        return res

    def post_image(self, img_path: str, parse: bool = True):
        headers = self.get_headers()
        boundary = "FormBoundaryXYZ"
        headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
        with open(img_path, "rb") as h:
            img_data = h.read()
        body = (
            "--"
            + boundary
            + "\r\n"
            + 'Content-Disposition: form-data; name="image"; filename="'
            + os.path.basename(img_path)
            + '"\r\n'
            + "Content-Type: "
            + mimetypes.guess_type(img_path)[0]
            + "\r\n\r\n"
            + img_data.decode("latin1")
            + "\r\n"
            + "--"
            + boundary
            + "--\r\n"
        )
        res = self.post("/v1/images", body=body, headers=headers, parse=parse)
        return res

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
        }

    def __enter__(self):
        super().__enter__()
        self.me = self.get_me()["data"]
        return self
