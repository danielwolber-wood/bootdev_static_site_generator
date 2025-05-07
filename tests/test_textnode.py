import unittest
from src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):

    def test_equal_nodes(self):
        node1 = TextNode("Sample", TextType.TEXT)
        node2 = TextNode("Sample", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("Sample", TextType.TEXT)
        node2 = TextNode("Different", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_type(self):
        node1 = TextNode("Sample", TextType.TEXT)
        node2 = TextNode("Sample", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Sample", TextType.LINK, url="https://example.com")
        node2 = TextNode("Sample", TextType.LINK, url="https://other.com")
        self.assertNotEqual(node1, node2)

    def test_equal_with_none_url(self):
        node1 = TextNode("Sample", TextType.ITALIC, url=None)
        node2 = TextNode("Sample", TextType.ITALIC, url=None)
        self.assertEqual(node1, node2)

    def test_not_equal_none_vs_string_url(self):
        node1 = TextNode("Sample", TextType.LINK, url=None)
        node2 = TextNode("Sample", TextType.LINK, url="https://example.com")
        self.assertNotEqual(node1, node2)

    def test_repr_output(self):
        node = TextNode("Hello", TextType.BOLD, url="https://hello.com")
        expected_repr = "TextNode(Hello, bold, https://hello.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_output_no_url(self):
        node = TextNode("World", TextType.TEXT)
        expected_repr = "TextNode(World, text, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_all_text_types(self):
        for text_type in TextType:
            node = TextNode("Example", text_type)
            self.assertEqual(node.text_type, text_type)

if __name__ == "__main__":
    unittest.main()
