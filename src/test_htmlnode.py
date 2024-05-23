import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_propstohtml(self):
        node = HTMLNode("div", {"class": "test"}, "test")
        self.assertEqual(node.props_to_html(), ' class="test"')

    def test_propstohtmlnull(self):
        node = HTMLNode("h1")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    # we need to test two things:
    # - the function have deterministic output
    # - if it still works with no props

    def test_tohtml(self):
        node = LeafNode("h1", "Hello", {"class": "test"})
        self.assertEqual(node.to_html(), '<h1 class="test">Hello</h1>')

    def test_tohtmlnull(self):
        node = LeafNode("h1", "Hello")
        self.assertEqual(node.to_html(), "<h1>Hello</h1>")


class TestParentNode(unittest.TestCase):
    # we need to test if tohtml works as intended

    def test_tohtml(self):
        node = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        res = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), res)

    # what if we pass two parent nodes?
    def test_tohtml2(self):
        node = ParentNode(
            "p",
            children=[
                ParentNode(
                    "div",
                    children=[
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        res = (
            "<p><div><b>Bold text</b>Normal text</div><i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node.to_html(), res)

    # what if we don't pass any values?
    def test_tohtmlnull(self):
        node = ParentNode("p", children=[], props=None)
        self.assertEqual(node.to_html(), "<p></p>")
