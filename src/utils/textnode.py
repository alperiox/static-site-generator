from ..enums import TextNodeTypes
from ..textnode import TextNode
from .markdown import extract_markdown_images, extract_markdown_links


def split_text_node_delimiter(
    node: TextNode, delimiter: str, text_type: str
) -> list[TextNode]:
    # this function won't work if the text node has both * and ** in it.
    nodes = []
    Ld = len(delimiter)
    if delimiter in node.text:
        text = node.text
        while delimiter in text:
            start_ix = text.index(delimiter)
            try:
                end_ix = text[start_ix + Ld :].index(delimiter) + start_ix + Ld
            except ValueError:
                raise ValueError(f"Delimiter {delimiter} not closed in text: {text}")

            first_part = text[:start_ix]
            part = text[start_ix + Ld : end_ix]
            second_part = text[end_ix + Ld :]

            if len(first_part) > 0:
                nodes.append(TextNode(first_part, TextNodeTypes.TEXT))

            nodes.append(TextNode(part, text_type))

            text = second_part
        if len(text) > 0:
            nodes.append(TextNode(text, TextNodeTypes.TEXT))
    else:
        nodes.append(node)
    return nodes


def split_text_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        nodes = split_text_node_delimiter(node, delimiter, text_type)
        new_nodes.extend(nodes)
    return new_nodes


def split_nodes_image_or_link(
    old_nodes: list[TextNode], text_type: str
) -> list[TextNode]:
    if text_type not in [TextNodeTypes.IMAGE, TextNodeTypes.LINK]:
        raise ValueError(
            f"text_type must be either '{TextNodeTypes.IMAGE}' or '{TextNodeTypes.LINK}'"
        )
    elif text_type == TextNodeTypes.IMAGE:
        fn = extract_markdown_images
        extra_char = "!"
    elif text_type == TextNodeTypes.LINK:
        fn = extract_markdown_links
        extra_char = ""

    def splitter(old_nodes: list[TextNode]) -> list[TextNode]:
        nodes = []
        for old_node in old_nodes:
            text = old_node.text
            parts = fn(text)
            if len(parts) == 0:
                nodes.append(old_node)
                continue
            for part in parts:
                part_text = extra_char + f"[{part[0]}]({part[1]})"
                start_ix = text.index(part_text)
                first_part = text[:start_ix]
                if len(first_part) > 0:
                    nodes.append(TextNode(first_part, TextNodeTypes.TEXT))
                nodes.append(TextNode(part[0], text_type, part[1]))
                text = text[start_ix + len(part_text) :]
            if len(text) > 0:
                nodes.append(TextNode(text, TextNodeTypes.TEXT))
        return nodes

    return splitter(old_nodes)


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = ["**", "*", "`"]
    names = [TextNodeTypes.BOLD, TextNodeTypes.ITALIC, TextNodeTypes.CODE]
    nodes = [TextNode(text, TextNodeTypes.TEXT)]

    for delimiter, name in zip(delimiters, names):
        nodes = split_text_nodes_delimiter(nodes, delimiter, name)
    nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)
    nodes = split_nodes_image_or_link(nodes, TextNodeTypes.LINK)

    return nodes
