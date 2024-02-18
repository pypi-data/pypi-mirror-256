from typing import Dict
from pprint import pprint
import warnings
import re
import requests
import json

import unicodeit as ucit


def _reformat(src: str) -> str:
    def _replace(match):
        return "\\%s{%s}%s" % (match.group(1), match.group(2)[0], match.group(2)[1:])

    pattern = r"\\([a-zA-Z_]+)\s+([a-zA-Z0-9^]+)"
    return re.sub(pattern, _replace, src)


def _split_on_dbl_slash(src: str) -> str:
    return src.split(r"\\")


def tex2image(tex: str):
    url = "https://e1kf0882p7.execute-api.us-east-1.amazonaws.com/default/latex2image"
    payload = {
        "latexInput": "\\begin{align*}\n" + tex + "\n\\end{align*}\n",
        "outputFormat": "PNG",
        "outputScale": "125%",
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers)
    if not res.ok:
        raise
    res = res.json()
    if res["error"] is not None:
        raise
    return res["imageUrl"]


class NotionRender:
    def __init__(self, callbacks=[]) -> None:
        self.callbacks = callbacks

    def render(self, target: Dict) -> dict:
        output = dict()
        output["content"] = []
        output["title"] = target["child_page"]["title"]
        stack = [target]
        while stack:
            node = stack.pop()
            for cb in self.callbacks:
                cb(node)
            # print(node)
            tp = node["type"]

            # visit current node
            if tp == "child_page":
                output["content"].append(self.handle_child_page(node[tp]))
            elif tp == "paragraph":
                output["content"].append(self.handle_paragraph(node[tp]))
            elif tp.startswith("heading"):
                level = int(tp.split("_")[-1])
                output["content"].append(self.handle_heading(node[tp], level))
            elif tp == "code":
                output["content"].append(self.handle_code(node[tp]))
            elif tp == "image":
                output["content"].append(self.handle_image(node[tp]))
            elif tp == "equation":
                print(node[tp])
                output["content"].append(self.handle_equation(node[tp]))
            else:
                warnings.warn(f"Unrecognized block type: {tp}")

            # push children to stack
            for child in node.get("children", dict()).get("results", [])[::-1]:
                stack.append(child)
        output["content"] = "\n".join(output["content"])
        return output

    def handle_child_page(self, content: dict) -> str:
        return f'<h1>{content["title"]}</h1>'

    def handle_paragraph(self, content: dict) -> str:
        return self.handle_rich_text(content["rich_text"])

    def handle_rich_text(self, content: dict) -> str:
        # assert block['type'] == 'rich_text', block['type']
        # content = node['rich_text']
        output = []
        for text in content:
            tp = text["type"]
            text_content = text[tp]
            if tp == "text":
                output.append(self.handle_text(text_content))
            elif tp == "equation":
                output.append(self.handle_inline_equation(text_content, no_tag=True))
            else:
                warnings.warn(f"Unrecognized rich text type: {tp}")
        return f'<p>{"".join(output)}</p>'

    def handle_text(self, content: dict) -> str:
        return f'{content["content"]}'

    def handle_equation(self, content: dict) -> str:
        # convert tex to image
        imgUrl = tex2image(content["expression"])
        return f"<img src={imgUrl}>"

    def handle_inline_equation(self, content: dict, no_tag: bool = False) -> str:
        tex = _reformat(content["expression"])
        print(tex)
        uni = ucit.replace(tex)
        print(uni)
        uni = _split_on_dbl_slash(uni)
        if no_tag:
            return ", ".join(uni)
        return "".join([f"<p>{u}</p>" for u in uni])

    def handle_heading(self, content: dict, level: int) -> str:
        text = self.handle_rich_text(content["rich_text"])
        return f"<h{level}>\n{text}\n</h{level}>"

    def handle_code(self, content: dict, level: int) -> str:
        text = self.handle_rich_text(content["rich_text"])
        return f"<pre>\n{text}\n</pre>"

    def handle_image(self, content: dict, level: int) -> str:
        return f'<img src="{content["file"]["url"]}">'
