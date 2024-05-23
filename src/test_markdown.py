import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.utils.markdown import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html,
)


class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "![image1](path/to/image1.png) ![image2](path/to/image2.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image1", "path/to/image1.png"), ("image2", "path/to/image2.png")],
        )

    def test_extract_markdown_links(self):
        text = "[link1](path/to/link1) [link2](path/to/link2)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link1", "path/to/link1"), ("link2", "path/to/link2")],
        )

    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""

        blocks = markdown_to_blocks(text)

        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    # what if there are multiple spaces between blocks?
    def test_markdown_to_blocks(self):
        text = """# This is a heading

        
This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is a list item
* This is another list item
"""

        blocks = markdown_to_blocks(text)

        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    # what if the text is just empty string?
    def test_markdown_to_blocks_empty(self):
        text = ""

        blocks = markdown_to_blocks(text)

        self.assertEqual(blocks, [])

    # what if the text is just a few whitespaces?
    def test_markdown_to_blocks_whitespaces(self):
        text = "   "

        blocks = markdown_to_blocks(text)

        self.assertEqual(blocks, [])

    # test the block_to_block_type function
    def test_block_to_block_type(self):
        text = """# This is a heading 

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

``` 
this is a code block
```

> This is a quote block

* This is a list item

1. This is an ordered list item
"""

        blocks = markdown_to_blocks(text)
        block_types = [block_to_block_type(block) for block in blocks]

        self.assertEqual(
            block_types,
            [
                "heading",
                "paragraph",
                "code",
                "quote",
                "unordered_list",
                "ordered_list",
            ],
        )

    # testing the markdown_to_html function
    def test_markdown_to_html(self):
        text = """# This is a heading
        
This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item

```
print("this is a code block for the test")
```

> This is a quote block

### This is a subheading

Here are some ordered items

1. This is the first item
2. This is the second item
"""
        htmlnodes = markdown_to_html(text)

        self.assertEqual(
            htmlnodes,
            ParentNode(
                tag="div",
                children=[
                    LeafNode(tag="h1", value="This is a heading"),
                    LeafNode(
                        tag="p",
                        value="This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    ),
                    ParentNode(
                        tag="ul",
                        children=[
                            LeafNode(tag="li", value="This is a list item"),
                            LeafNode(tag="li", value="This is another list item"),
                        ],
                    ),
                    ParentNode(
                        tag="pre",
                        children=[
                            LeafNode(
                                tag="code",
                                value='\nprint("this is a code block for the test")\n',
                            )
                        ],
                    ),
                    LeafNode(tag="blockquote", value="This is a quote block"),
                    LeafNode(tag="h3", value="This is a subheading"),
                    LeafNode(tag="p", value="Here are some ordered items"),
                    ParentNode(
                        tag="ol",
                        children=[
                            LeafNode(tag="li", value="This is the first item"),
                            LeafNode(tag="li", value="This is the second item"),
                        ],
                    ),
                ],
            ),
        )

    # what if the text is just empty string?
    def test_markdown_to_html_empty(self):
        text = ""

        htmlnodes = markdown_to_html(text)

        self.assertEqual(htmlnodes, ParentNode("div", children=[]))
