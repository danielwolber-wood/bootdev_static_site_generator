from itertools import zip_longest
import re

from dataclasses import dataclass
from .textnode import TextNode, TextType
from .htmlnode import LeafNode

def text_node_to_html_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(value=node.text, tag="")
        case TextType.ITALIC:
            return LeafNode(value=node.text, tag="i")
        case TextType.BOLD:
            return LeafNode(value=node.text, tag="b")
        case TextType.CODE:
            return LeafNode(value=node.text, tag="code")
        case TextType.LINK:
            return LeafNode(value=node.text, tag="a", props={"href": node.url})
        case TextType.IMAGE:
            return LeafNode(value="", tag="img", props={"src": node.url, "alt": node.text})
        case _:
            raise ValueError()

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    all_new_nodes = list()
    for old_node in old_nodes:
        initial_delimiter = (old_node.text[0] == delimiter)
        final_delimiter = (old_node.text[-1] == delimiter)
        split_string = old_node.text.split(delimiter)
        # first, if the length is even, then there was an odd number of delimiters, and should raise an error
        if len(split_string) % 2 == 0:
            raise ValueError
        # if there is an initial delimiter, l[0] will be ''
        # if there is a final delimiter, l[-1] will be ''
        # in either case, every odd element will be a match
        new_nodes = list()
        for index, item in enumerate(split_string):
            if index %2 == 1:
                this_type = text_type
            else:
                this_type = old_node.text_type # nonmatching should inherit type of containing node
            new_node = TextNode(text=item,text_type=this_type,url=None)
            new_nodes.append(new_node)

        if new_nodes[0].text == "":
            new_nodes = new_nodes[1:]
        if new_nodes[-1].text == "":
            new_nodes = new_nodes[:-1]
        all_new_nodes.extend(new_nodes)
    return all_new_nodes

@dataclass
class RegexMatch:
    start: int
    end: int
    url: str
    alt_text: str
    text_type:TextType

@dataclass
class NonMatch:
    start: int
    end: int
    text_type: TextType

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    """Finds and extract all markdown images and alt text using regex
    Format must match ![alt-text](http://url/a.png)
    """

    return_list = list()
    pattern =  r"!\[(.*?)\]\((.*?)\)"
    matches = re.finditer(pattern, text)

    for m in matches:
        #print(f'match is {m.group(0)}')  # full match
        #print(f'start, end: {m.start()}, {m.end()}')
        #print(f'alt text is: {m.group(1)}')
        #print(f'URL is: {m.group(2)}')
        return_list.append((m.group(1), m.group(2)))

    return return_list

def split_node_image(old_node:TextNode) -> list[TextNode]:
    text = old_node.text
    pattern =  r"!\[(.*?)\]\((.*?)\)"
    matches = list(re.finditer(pattern, text))
    new_nodes = list()

    previous_end = 0
    if not matches:
        return [old_node]
    for m in matches:
        #print(f'match is {m.group(0)}')  # full match
        #print(f'start, end: {m.start()}, {m.end()}')
        #print(f'alt text is: {m.group(1)}')
        #print(f'URL is: {m.group(2)}')
        prior_nonmatching_text = text[previous_end:m.start()]
        prior_node = TextNode(text=prior_nonmatching_text, text_type=old_node.text_type, url=None)
        image_node = TextNode(text=m.group(1), url=m.group(2), text_type=TextType.IMAGE)
        new_nodes.append(prior_node)
        new_nodes.append(image_node)
        previous_end = m.end()
        #regex_match = RegexMatch(start=m.start(), end=m.end(), alt_text=m.group(1), url=m.group(2), text_type=TextType.IMAGE)
        #regex_matches.append(regex_match)
    return new_nodes


def split_node_regex(old_node:TextNode, split_type:TextType) -> list[TextNode]:
    text = old_node.text
    if split_type == TextType.LINK:
        pattern =  r"\[(.*?)\]\((.*?)\)"
    elif split_type == TextType.IMAGE:
        pattern = r"!\[(.*?)\]\((.*?)\)"
    else:
        raise ValueError()

    matches = list(re.finditer(pattern, text))
    new_nodes = list()

    previous_end = 0
    if not matches:
        return [old_node]
    for m in matches:
        ##print(f'match is {m.group(0)}')  # full match
        ##print(f'start, end: {m.start()}, {m.end()}')
        ##print(f'alt text is: {m.group(1)}')
        ##print(f'URL is: {m.group(2)}')
        prior_nonmatching_text = text[previous_end:m.start()]
        prior_node = TextNode(text=prior_nonmatching_text, text_type=old_node.text_type, url=None)
        image_node = TextNode(text=m.group(1), url=m.group(2), text_type=split_type)
        if prior_node.text == "":
            pass
        else:
            new_nodes.append(prior_node)
        new_nodes.append(image_node)
        previous_end = m.end()
        #regex_match = RegexMatch(start=m.start(), end=m.end(), alt_text=m.group(1), url=m.group(2), text_type=TextType.IMAGE)
        #regex_matches.append(regex_match)

    # add the rest of the text as a final node
    if previous_end != len(text):
        end_text = text[previous_end:]
        new_nodes.append(TextNode(text=end_text, text_type=old_node.text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    all_nodes = list()
    for old_node in old_nodes:
        all_nodes.extend(split_node_regex(old_node, split_type=TextType.IMAGE))
    return all_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    all_nodes = list()
    for old_node in old_nodes:
        all_nodes.extend(split_node_regex(old_node, split_type=TextType.LINK))
    return all_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
    nodes = [TextNode(text_type=TextType.TEXT, text=text)]
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="`", text_type=TextType.CODE)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(s:str) -> list[str]:
    segments = s.split("\n\n")
    segments = [s.strip() for s in segments]
    segments = [s for s in segments if s != ""]
    return segments