from ..enums import TextNodeTypes
from ..htmlnode import HTMLNode, LeafNode
from ..textnode import TextNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    available_types = TextNodeTypes.get()

    if text_node.text_type not in available_types:
        raise ValueError(
            f"Invalid text type: {text_node.text_type}, must be one of {available_types}"
        )
    if text_node.text_type == TextNodeTypes.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextNodeTypes.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextNodeTypes.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextNodeTypes.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextNodeTypes.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextNodeTypes.IMAGE:
        return LeafNode(
            tag="img", value=None, props={"src": text_node.url, "alt": text_node.text}
        )
