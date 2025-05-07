from typing import Optional

class HTMLNode:
    def __init__(self, tag:Optional[str]=None, value:Optional[str]=None, children:Optional[list]=None, props:Optional[dict]=None) -> None:
        """tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}"""
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        fragments = [f'{key}="{value}"' for key, value in self.props.items()]
        return " ".join(fragments)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag:Optional[str], value:str, props:Optional[dict]=None) -> None:
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        """E.g.,
        LeafNode("p", "This is a paragraph of text.").to_html() -> "<p>This is a paragraph of text.</p>"""
        if self.value is None:
            raise ValueError

        if self.props is None or len(self.props) == 0:
            prop_string = ""
        else:
            prop_fragments = [f'{key}="{value}"' for key, value in self.props.items()]
            prop_string = " " +  " ".join(prop_fragments)

        self_closing_tags = {"img", "br", "hr", "input", "meta", "link"}
        if self.tag is None or self.tag == "":
            return self.value
        elif self.tag in self_closing_tags:
            return f'<{self.tag}{prop_string}/>'
        else:
            return f'<{self.tag}{prop_string}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:Optional[dict]=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        """
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
->
<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
        """
        if self.tag is None:
            raise ValueError
        if self.children is None or len(self.children) == 0:
            raise ValueError
        fragments = [child.to_html() for child in self.children]
        fragments = [f for f in fragments if f is not None]
        if len(fragments) > 0 and fragments is not None:
            inner_string = "".join(fragments)
        else:
            inner_string = ""
        start = f"<{self.tag}>"
        end = f"</{self.tag}>"
        return start + inner_string + end