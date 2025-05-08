import unittest

from src.utils import split_nodes_delimiter, extract_markdown_images, text_node_to_html_node, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from src.textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("Sample text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Sample text")
        self.assertEqual(html_node.tag, "")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
        self.assertEqual(html_node.tag, "i")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
        self.assertEqual(html_node.tag, "b")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>Code text</code>")
        self.assertEqual(html_node.tag, "code")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_link(self):
        node = TextNode("Link text", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Link text</a>')
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.png" alt="Alt text"/>')
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})

    def test_text_node_to_html_node_invalid_type(self):
        node = TextNode("Invalid type", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        ##print("\n")
        ##print("Test 1")
        # Test with a basic code block
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        ##print(f"node is {node}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple(self):
        ##print("\n")
        ##print("Test 2")
        # Test with multiple code blocks
        node = TextNode("Here is `code1` and `code2` in text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        ##print(f"node is {node}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Here is ")
        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " in text")

    def test_split_nodes_delimiter_no_match(self):
        # No delimiters to match
        ##print("\n")
        ##print("Test 3")
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        ##print(f"node is {node}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text with no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_starts_with(self):
        ##print("\n")
        ##print("Test 4")
        # Text starts with delimiter
        node = TextNode("`code` followed by text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        ##print(f"node is {node}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " followed by text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_ends_with(self):
        ##print("\n")
        ##print("Test 5")
        # Text ends with delimiter
        node = TextNode("text followed by `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        ##print(f"node is {node}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "text followed by ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_split_nodes_delimiter_multiple_nodes(self):
        ###print("\n")
        ###print("Test 6")
        # Multiple nodes in input
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("More text", TextType.TEXT)
        node3 = TextNode("Even more `code blocks` here", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        ###print(f"node1 is {node1}")
        ###print(f"node2 is {node2}")
        ###print(f"node3 is {node3}")
        ###print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, "More text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "Even more ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "code blocks")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)
        self.assertEqual(new_nodes[5].text, " here")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_non_text_node(self):
        ##print("\n")
        ##print("Test 7")
        # Input includes non-TEXT type nodes
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("Bold text", TextType.BOLD)
        node3 = TextNode("More `code`", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        ##print(f"node1 is {node1}")
        ##print(f"node2 is {node2}")
        ##print(f"node3 is {node3}")
        ##print(f"new_nodes is {new_nodes}")

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, "Bold text")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "More ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "code")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image ![Alt text](http://example.com/image.png)"
        expected = [("Alt text", "http://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = """
        ![First Image](http://example.com/first.png)
        Some text in between.
        ![Second Image](http://example.com/second.jpg)
        """
        expected = [
            ("First Image", "http://example.com/first.png"),
            ("Second Image", "http://example.com/second.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_images_with_varied_formats(self):
        text = "![A scenic mountain view](https://example.com/images/mountain.jpg)\n" \
               "![City Skyline at Night](https://example.com/images/city-skyline.jpeg)"
        expected = [
            ("A scenic mountain view", "https://example.com/images/mountain.jpg"),
            ("City Skyline at Night", "https://example.com/images/city-skyline.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This paragraph has no images, just plain text."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text(self):
        text = "Here is an image with no alt text ![](http://example.com/blank.png)"
        expected = [("", "http://example.com/blank.png")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link_at_start(self):
        #print("\n\n")
        #print('test 1')
        node = TextNode("[Boot Dev](https://www.boot.dev) is great", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        #print(f'new_nodes is {new_nodes}')
        self.assertListEqual(
            [
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            new_nodes,
        )
        #print("\n\n")

    def test_single_link_at_end(self):
        node = TextNode("Visit [Boot Dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_adjacent_links(self):
        node = TextNode("[A](url1)[B](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A", TextType.LINK, "url1"),
                TextNode("B", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_link_with_special_characters(self):
        node = TextNode(
            "Check [this](https://example.com/path?query=1&value=something#anchor)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("this", TextType.LINK, "https://example.com/path?query=1&value=something#anchor"),
            ],
            new_nodes,
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    """
    def test_malformed_link_missing_closing_paren(self):
        node = TextNode("Go to [Boot Dev](https://www.boot.dev", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_malformed_link_missing_brackets(self):
        node = TextNode("Go to Boot Dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        """

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First [Link1](http://1.com)", TextType.TEXT),
            TextNode("Second [Link2](http://2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("Link1", TextType.LINK, "http://1.com"),
                TextNode("Second ", TextType.TEXT),
                TextNode("Link2", TextType.LINK, "http://2.com"),
            ],
            new_nodes,
        )

"""
    def test_link_with_parentheses_in_url(self):
        node = TextNode(
            "See [example](https://en.wikipedia.org/wiki/Function_(mathematics))",
            TextType.TEXT,
        )
        # This test will *fail* unless you update your regex to handle nested parentheses
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("example", TextType.LINK, "https://en.wikipedia.org/wiki/Function_(mathematics)"),
            ],
            new_nodes,
        )
        """


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual_nodes = text_to_textnodes(text)
        self.assertEqual(actual_nodes, expected_nodes)

    """
    def test_empty_string(self):
        text = ""
        expected_nodes = []
        actual_nodes = text_to_textnodes(text)
        self.assertEqual(actual_nodes, expected_nodes)
    """

    def test_only_plain_text(self):
        text = "Just plain text without any markdown"
        expected_nodes = [TextNode("Just plain text without any markdown", TextType.TEXT)]
        actual_nodes = text_to_textnodes(text)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_multiple_same_type(self):
        text = "**Bold text** and more **bold text**"
        expected_nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(" and more ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD)
        ]
        actual_nodes = text_to_textnodes(text)
        self.assertEqual(actual_nodes, expected_nodes)

    """
    def test_nested_markdown(self):
        # This tests how your function handles potentially nested markdown
        # Most simple parsers would treat this as alternating formatting
        text = "**Bold _and italic_**"
        expected_nodes = [
            TextNode("Bold ", TextType.BOLD),
            TextNode("and italic", TextType.ITALIC),
            TextNode("", TextType.BOLD)
        ]
        actual_nodes = text_to_textnodes(text)
        self.assertEqual(actual_nodes, expected_nodes)
        """

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        md = "Just a single block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block"])

    def test_blocks_separated_by_blank_line(self):
        md = "First block\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_trailing_and_leading_whitespace(self):
        md = "\n\nBlock with whitespace\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with whitespace"])

    def test_multiple_newlines_between_blocks(self):
        md = "Block1\n\n\n\nBlock2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block1", "Block2"])

    def test_example_from_assignment(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()

