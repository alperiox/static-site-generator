import unittest

from src.enums import TextNodeTypes
from src.utils.textnode import (
    split_nodes_image_or_link,
    split_text_nodes_delimiter,
    text_to_textnodes,
)
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("test node", TextNodeTypes.BOLD)
        node2 = TextNode("test node", TextNodeTypes.BOLD)

        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("test node", TextNodeTypes.BOLD)
        node2 = TextNode("test node", TextNodeTypes.ITALIC)

        self.assertNotEqual(node, node2)

    # test if splitting text nodes based on different delimiters work
    def test_split_nodes_delimiter_single(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextNodeTypes.CODE),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "`", TextNodeTypes.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
                TextNode(" word", TextNodeTypes.TEXT),
            ],
        )

    # what if we have two blocks
    def test_split_nodes_delimiter_double(self):
        nodes = [
            TextNode(
                "This is text with a `code block` word and another `code block`",
                TextNodeTypes.CODE,
            ),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "`", TextNodeTypes.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
                TextNode(" word and another ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
            ],
        )

    # what if the block is at the start
    def test_split_nodes_delimiter_start(self):
        nodes = [
            TextNode("`code block` word and another `code block`", TextNodeTypes.CODE),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "`", TextNodeTypes.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code block", TextNodeTypes.CODE),
                TextNode(" word and another ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
            ],
        )

    # what if there are two block next to each other
    def test_split_nodes_delimiter_next(self):
        nodes = [
            TextNode("`code block``code block`", TextNodeTypes.CODE),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "`", TextNodeTypes.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code block", TextNodeTypes.CODE),
                TextNode("code block", TextNodeTypes.CODE),
            ],
        )

    # what if we have two different blocks?
    def test_split_nodes_delimiter_mix(self):
        nodes = [
            TextNode(
                "This is text with a `code block` word and *italic block*",
                TextNodeTypes.TEXT,
            ),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "`", TextNodeTypes.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
                TextNode(" word and *italic block*", TextNodeTypes.TEXT),
            ],
        )

    # what if a similar character to the delimiter is in the text?
    # this shouldn't work other way around.
    def test_split_nodes_delimiter_similar(self):
        nodes = [
            TextNode(
                "This is text with a **bold** word and *italic block*",
                TextNodeTypes.TEXT,
            ),
        ]

        new_nodes = split_text_nodes_delimiter(nodes, "**", TextNodeTypes.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("bold", TextNodeTypes.BOLD),
                TextNode(" word and *italic block*", TextNodeTypes.TEXT),
            ],
        )

    # test split_nodes_image function
    def test_split_nodes_image(self):
        nodes = [
            TextNode(
                "This is text with a ![image](path/to/image.png) word",
                TextNodeTypes.TEXT,
            ),
        ]

        new_nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("image", TextNodeTypes.IMAGE, "path/to/image.png"),
                TextNode(" word", TextNodeTypes.TEXT),
            ],
        )

    # what if there are more images in the text?
    def test_split_nodes_image_multiple(self):
        nodes = [
            TextNode(
                "This is text with a ![image](path/to/image.png) word and another ![image](path/to/image.png)",
                TextNodeTypes.TEXT,
            ),
        ]

        new_nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("image", TextNodeTypes.IMAGE, "path/to/image.png"),
                TextNode(" word and another ", TextNodeTypes.TEXT),
                TextNode("image", TextNodeTypes.IMAGE, "path/to/image.png"),
            ],
        )

    # what if there are no images in the text?
    def test_split_nodes_image_none(self):
        nodes = [
            TextNode("This is text with a word", TextNodeTypes.TEXT),
        ]

        new_nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a word", TextNodeTypes.TEXT),
            ],
        )

    # what if there are no nodes?
    def test_split_nodes_image_empty(self):
        nodes = []

        new_nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)

        self.assertEqual(new_nodes, [])

    # what if the images are next to each other?
    def test_split_nodes_image_next(self):
        nodes = [
            TextNode(
                "This is text with a ![image](path/to/image.png)![image](path/to/image.png)",
                TextNodeTypes.TEXT,
            ),
        ]

        new_nodes = split_nodes_image_or_link(nodes, TextNodeTypes.IMAGE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNodeTypes.TEXT),
                TextNode("image", TextNodeTypes.IMAGE, "path/to/image.png"),
                TextNode("image", TextNodeTypes.IMAGE, "path/to/image.png"),
            ],
        )

    # test text to textnodes function
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextNodeTypes.TEXT),
                TextNode("text", TextNodeTypes.BOLD),
                TextNode(" with an ", TextNodeTypes.TEXT),
                TextNode("italic", TextNodeTypes.ITALIC),
                TextNode(" word and a ", TextNodeTypes.TEXT),
                TextNode("code block", TextNodeTypes.CODE),
                TextNode(" and an ", TextNodeTypes.TEXT),
                TextNode(
                    "image",
                    TextNodeTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", TextNodeTypes.TEXT),
                TextNode("link", TextNodeTypes.LINK, "https://boot.dev"),
            ],
        )

    # what if we have a link, image, and code block next to each other?
    def test_text_to_textnodes_multiple(self):
        text = "This is a text with ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)[link](https://boot.dev)`code block`"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("This is a text with ", TextNodeTypes.TEXT),
                TextNode(
                    "image",
                    TextNodeTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode("link", TextNodeTypes.LINK, "https://boot.dev"),
                TextNode("code block", TextNodeTypes.CODE),
            ],
        )

    # it should just return the text if there are no special characters
    def test_text_to_textnodes_none(self):
        text = "This is a text with no special characters"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [TextNode("This is a text with no special characters", TextNodeTypes.TEXT)],
        )

    # what if there's an image and a link next to each other?
    def test_text_to_textnodes_image_link(self):
        text = "This is a text with ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)[link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("This is a text with ", TextNodeTypes.TEXT),
                TextNode(
                    "image",
                    TextNodeTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode("link", TextNodeTypes.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
