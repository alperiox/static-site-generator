class TextNodeTypes:
    TEXT = "text"
    IMAGE = "image"
    LINK = "link"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"

    @classmethod
    def get(cls):
        return [
            v for k, v in cls.__dict__.items() if not k.startswith("_") and k != "get"
        ]


class MarkdownBlockTypes:
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    @classmethod
    def get(cls):
        return [
            v for k, v in cls.__dict__.items() if not k.startswith("_") and k != "get"
        ]
