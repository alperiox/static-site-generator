import re

from ..enums import MarkdownBlockTypes
from ..htmlnode import HTMLNode, LeafNode, ParentNode


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    block = []
    lines = markdown.split("\n")
    for line in lines:
        if len(line.strip()) > 0:
            block.append(line)

        else:
            if len(block) > 0:
                blocks.append(block)
                block = []

    return ["\n".join(block) for block in blocks]


def block_to_block_type(markdown: str) -> str:
    lines = markdown.split("\n")

    if (
        markdown.startswith("# ")
        or markdown.startswith("## ")
        or markdown.startswith("### ")
        or markdown.startswith("#### ")
        or markdown.startswith("##### ")
        or markdown.startswith("###### ")
    ):
        return MarkdownBlockTypes.HEADING

    if len(lines) > 0 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return MarkdownBlockTypes.CODE

    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.QUOTE

    if markdown.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.UNORDERED_LIST

    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.UNORDERED_LIST

    if markdown.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.ORDERED_LIST

    return MarkdownBlockTypes.PARAGRAPH

def markdown_to_html(markdown: str) -> ParentNode:
    parent = ParentNode(tag="div", children=[])

    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    html_nodes = []

    for block, block_type in zip(blocks, block_types):
        if block_type == MarkdownBlockTypes.HEADING:
            html_nodes.append(_process_heading(block))

        if block_type == MarkdownBlockTypes.CODE:
            html_nodes.append(_process_code_block(block))

        if block_type == MarkdownBlockTypes.PARAGRAPH:
            html_nodes.append(_process_paragraphs(block))

        if block_type == MarkdownBlockTypes.QUOTE:
            html_nodes.append(_process_quotes(block))

        if block_type == MarkdownBlockTypes.UNORDERED_LIST:
            html_nodes.append(_process_unordered_list(block))

        if block_type == MarkdownBlockTypes.ORDERED_LIST:
            html_nodes.append(_process_ordered_list(block))

    parent.children = html_nodes

    return parent

def _process_value(value: str) -> list[LeafNode]:
    from .htmlnode import text_node_to_html_node
    from .textnode import text_to_textnodes

    text_nodes = text_to_textnodes(value)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def _process_unordered_list(unordered_list_block: str) -> HTMLNode:
    children = []
    for line in unordered_list_block.split("\n"):
        children.append(ParentNode(tag="li", children=_process_value(line[2:])))
    return ParentNode(tag="ul", children=children)


def _process_ordered_list(ordered_list_block: str) -> HTMLNode:
    children = []
    for line in ordered_list_block.split("\n"):
        children.append(ParentNode(tag="li", children=_process_value(line[3:])))
    return ParentNode(tag="ol", children=children)


def _process_code_block(code_block: str) -> HTMLNode:
    code_str = code_block.strip("```")

    code_element = LeafNode(tag="code", value=code_str)
    return ParentNode(tag="pre", children=[code_element])


def _process_heading(heading_block: str) -> HTMLNode:
    heading_level = 0
    for chr in heading_block:
        if chr == "#":
            heading_level += 1
        else:
            break

    heading_text = heading_block[heading_level + 1 :].strip()
    return ParentNode(tag=f"h{heading_level}", children=_process_value(heading_text))


def _process_paragraphs(paragraph_block: str) -> HTMLNode:
    return ParentNode(tag="p", children=_process_value(paragraph_block))


def _process_quotes(quote_block: str) -> HTMLNode:
    return ParentNode(
        tag="blockquote",
        children=_process_value("\n".join([line[2:] for line in quote_block.split("\n")])),
    )
