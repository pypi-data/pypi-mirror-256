if __name__ == "__main__":
    import os
    from notion2medium.converters import Converter

    with Converter(
        os.environ["NOTION_API_KEY"], os.environ["MEDIUM_API_KEY"]
    ) as convert:
        convert.pull_and_post(
            "1661463a8db24b6b8f6e52f8eda45a03", publishStatus="unlisted"
        )
