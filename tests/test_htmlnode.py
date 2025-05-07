import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_default_initialization(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_custom_initialization(self):
        children = [HTMLNode(tag="span", value="child")]
        props = {"class": "header", "id": "main"}
        node = HTMLNode(tag="div", value="Hello", children=children, props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"class": "btn", "disabled": "true", "id": "submit-button"})
        result = node.props_to_html()
        expected_fragments = [
            'class="btn"',
            'disabled="true"',
            'id="submit-button"',
        ]
        for fragment in expected_fragments:
            self.assertIn(fragment, result)
        self.assertEqual(len(result.split()), len(expected_fragments))

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_output(self):
        children = [HTMLNode(tag="span", value="child")]
        props = {"class": "btn"}
        node = HTMLNode(tag="div", value="Hello", children=children, props=props)
        expected_repr = ("HTMLNode(tag='div', value='Hello', "
                         f"children={repr(children)}, props={{'class': 'btn'}})")
        self.assertEqual(repr(node), expected_repr)


class TestLeafNode(unittest.TestCase):

    def test_to_html_with_tag(self):
        node = LeafNode(value="This is a paragraph.", tag="p")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")


    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_tag_value_and_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_to_html_with_self_closing_tag_and_props(self):
        node = LeafNode(tag="img", value="", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image"/>')

    def test_to_html_with_self_closing_tag_without_props(self):
        node = LeafNode(tag="br", value="", props=None)
        self.assertEqual(node.to_html(), "<br/>")

    def test_to_html_with_no_tag(self):
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_empty_tag(self):
        node = LeafNode(tag="", value="Standalone text")
        self.assertEqual(node.to_html(), "Standalone text")

    def test_to_html_with_empty_props_dict(self):
        node = LeafNode(tag="span", value="Label", props={})
        self.assertEqual(node.to_html(), "<span>Label</span>")

    def test_to_html_raises_value_error_on_none_value(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_tag(self):
        node = LeafNode(value="Just plain text", tag=None)
        self.assertEqual(node.to_html(), "Just plain text")

    def test_to_html_none_value_raises(self):
        node = LeafNode(value=None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_value_and_tag(self):
        node = LeafNode(value=None, tag=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_inherits_from_htmlnode(self):
        node = LeafNode(value="test", tag="span")
        self.assertIsInstance(node, HTMLNode)
        self.assertEqual(node.value, "test")
        self.assertEqual(node.tag, "span")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr_output(self):
        node = LeafNode(value="Hello", tag="strong")
        expected_repr = "HTMLNode(tag='strong', value='Hello', children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)


class TestParentNode(unittest.TestCase):

    def test_basic_rendering(self):
        node = ParentNode(
            "p",
            [
                LeafNode(value="Bold text", tag="b"),
                LeafNode(value="Normal text", tag=None),
                LeafNode(value="italic text", tag="i"),
                LeafNode(value="More normal", tag=None),
            ]
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>More normal</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_single_child(self):
        node = ParentNode(
            "div",
            [LeafNode(value="Hello", tag="span")]
        )
        expected_html = "<div><span>Hello</span></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_child_with_none_tag(self):
        node = ParentNode(
            "li",
            [LeafNode(value="Item 1", tag=None), LeafNode(value="Item 2", tag=None)]
        )
        expected_html = "<li>Item 1Item 2</li>"
        self.assertEqual(node.to_html(), expected_html)

    def test_nested_parents(self):
        inner = ParentNode(
            "ul",
            [
                ParentNode(tag="li", children=[LeafNode(value="One", tag=None)]),
                ParentNode(tag="li", children=[LeafNode(value="Two", tag=None)])
            ]
        )
        outer = ParentNode(tag="div", children=[inner])
        expected_html = "<div><ul><li>One</li><li>Two</li></ul></div>"
        self.assertEqual(outer.to_html(), expected_html)

    def test_tag_none_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(value="test", tag=None)]).to_html()

    def test_empty_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_children_none_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_repr_output(self):
        children = [LeafNode(value="child", tag=None)]
        node = ParentNode("section", children)
        expected_repr = f"HTMLNode(tag='section', value=None, children={repr(children)}, props=None)"
        self.assertEqual(repr(node), expected_repr)

    def test_mixed_leaf_and_parent_children(self):
        inner = ParentNode("span", [LeafNode(value="inner text", tag=None)])
        node = ParentNode("div", [LeafNode(value="Header", tag="h1"), inner])
        expected_html = "<div><h1>Header</h1><span>inner text</span></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_whitespace_and_empty_leaf(self):
        node = ParentNode("p", [LeafNode(value="", tag=None), LeafNode(value="Actual content", tag=None)])
        expected_html = "<p>Actual content</p>"
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
