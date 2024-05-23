import typing as t


class HTMLNode:
    def __init__(self, tag, props=None, value=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, HTMLNode) and self.__dict__ == other.__dict__:
            return True

    def props_to_html(self):
        if self.props:
            return " " + " ".join(
                [f'{key}="{value}"' for key, value in self.props.items()]
            )
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.props}, {self.value}, {self.children})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, props, value)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.props}, {self.value}, {self.children})"

    def to_html(self):
        if self.tag:
            html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            html_string = f"{self.value}"

        return html_string


class ParentNode(HTMLNode):
    def __init__(self, tag=None, props=None, value=None, children=None):
        super().__init__(tag, props, value, children)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.props}, {self.value}, {self.children})"

    def to_html(self):
        if not isinstance(self.children, t.Union[list, tuple, LeafNode, ParentNode]):
            raise ValueError("ParentNode must have children")
        if not self.tag:
            raise ValueError("ParentNode must have a tag")

        tagstart = f"<{self.tag}{self.props_to_html()}>"
        text = ""
        tagend = f"</{self.tag}>"

        for child in self.children:
            text += child.to_html()

        return tagstart + text + tagend
