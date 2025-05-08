import re
import pathlib

from blocktype import BlockType
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode


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

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    """Finds and extract all markdown images and alt text using regex
    Format must match ![alt-text](http://url/a.png)
    """

    return_list = list()
    pattern =  r"!\[(.*?)\]\((.*?)\)"
    matches = re.finditer(pattern, text)

    for m in matches:
        ##print(f'match is {m.group(0)}')  # full match
        ##print(f'start, end: {m.start()}, {m.end()}')
        ##print(f'alt text is: {m.group(1)}')
        ##print(f'URL is: {m.group(2)}')
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
        ##print(f'match is {m.group(0)}')  # full match
        ##print(f'start, end: {m.start()}, {m.end()}')
        ##print(f'alt text is: {m.group(1)}')
        ##print(f'URL is: {m.group(2)}')
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
        ###print(f'match is {m.group(0)}')  # full match
        ###print(f'start, end: {m.start()}, {m.end()}')
        ###print(f'alt text is: {m.group(1)}')
        ###print(f'URL is: {m.group(2)}')
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

def block_to_blocktype(s:str) -> BlockType:
    """Identifies a block of markdown text as a paragraph, heading, code block, block quote, ordered list, or unordered list"""
    if s == "":
        return BlockType.PARAGRAPH

    if s[:3] == '```' and s[-3:] == "```":
        return BlockType.CODE

    lines = s.split("\n")
    quote_lines = [x for x in lines if x[0] == ">"]

    if len(quote_lines) == len(lines):
        return BlockType.QUOTE

    unordered_list = [x for x in lines if x[:2] == "* " or x[:2] == "+ " or x[:2] == "- "]

    if len(unordered_list) == len(lines):
        return BlockType.UNORDERED_LIST

    heading_regex = r"^#{1,6} \w+"
    heading_match = re.match(pattern=heading_regex, string=lines[0])
    if heading_match:
        return BlockType.HEADING

    for index, item in enumerate(lines):
        ordered_list_start = f"{index+1}. "
        item_start = item[:len(ordered_list_start)]
        if item_start == ordered_list_start:
            continue
        else:
            break
    else:
        return BlockType.ORDERED_LIST



    return BlockType.PARAGRAPH

def text_to_children(s:str) -> list[LeafNode]:
    textnodes = text_to_textnodes(s)
    htmlnodes = list()
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(textnode)
        htmlnodes.append(htmlnode)
    return htmlnodes


def block_to_paragraph_node(block:str) -> ParentNode:
    block = block.replace("\n", " ").strip() # only code block should retain newlines etc
    children = text_to_children(block)
    tag = "p"
    return ParentNode(tag=tag, children=children)

def block_to_heading_node(block:str) -> ParentNode:
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    content = block[level:].strip().replace("\n", " ")
    tag = f"h{level}"
    children = text_to_children(content)
    return ParentNode(tag=tag, children=children)

def block_to_code_node(block:str) -> ParentNode:
    # should be a <code> block nested inside a <pre> block
    lines = block.split("\n")
    code_content = "\n".join(lines[1:-1]) #remove backticks
    text_node = TextNode(code_content, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    inner_node = ParentNode(tag="code", children=[code_node])
    return ParentNode(tag="pre", children=[inner_node])

def block_to_block_quote_node(block:str) -> ParentNode:
    lines = block.split("\n")
    cleaned_lines = list()
    for line in lines:
        #line = line.replace("> ", "")
        if line.startswith("> "):
            line = line[2:]
        elif line.startswith(">"):
            line = line[1:]
        cleaned_lines.append(line)
    quote_content = " ".join(cleaned_lines).strip()
    children = text_to_children(quote_content)
    tag = "blockquote"
    return ParentNode(tag=tag, children=children)

def block_to_unordered_list_node(block:str) -> ParentNode:
    lines = block.split("\n")
    line_nodes = list()
    for line in lines:
        if not line.strip():
            continue
        line = line[2:].strip() # remove leading "* ", "+ " and "- "
        children = text_to_children(line)
        line_node = ParentNode(tag="li", children=children)
        line_nodes.append(line_node)

    return ParentNode(tag="ul", children=line_nodes)

def block_to_ordered_list_node(block:str) -> ParentNode:
    lines = block.split("\n")
    line_nodes = list()
    for line in lines:
        if not line.strip():
            continue
        # remove leading digit, dot, and space
        pieces = line.split(".")
        rejoined = ".".join(pieces[1:]).strip()
        children = text_to_children(rejoined)
        line_node = ParentNode(tag="li", children=children)
        line_nodes.append(line_node)

    return ParentNode(tag="ol", children=line_nodes)

def markdown_to_html_node(s:str) -> ParentNode:

    parent = ParentNode("div", children=list(),props=list())

    if s == "":
        return parent

    blocks  = markdown_to_blocks(s)
    for block in blocks:
        block_type = block_to_blocktype(block)
        #print("\n")
        #print(f"block is {block}")
        #print(f"block_type is {block_type}")
        match block_type:
            case BlockType.PARAGRAPH:
                new_node = block_to_paragraph_node(block)
            case BlockType.HEADING:
                new_node = block_to_heading_node(block)
            case BlockType.CODE:
                new_node = block_to_code_node(block)
            case BlockType.ORDERED_LIST:
                new_node = block_to_ordered_list_node(block)
            case BlockType.UNORDERED_LIST:
                new_node = block_to_unordered_list_node(block)
            case BlockType.QUOTE:
                new_node = block_to_block_quote_node(block)
            case _:
                raise ValueError
        parent.children.append(new_node)

    return parent

def extract_title(markdown:str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            #print("match found")
            match = line[2:].strip()
            #print(f"match is {match}")
            return match

    raise ValueError

def generate_page(from_path: pathlib.Path, template_path: pathlib.Path, dest_path:pathlib.Path, basepath: str) -> None:
    print(f"generating page {str(from_path)} to {str(dest_path)} using {str(template_path)}")

    with open(from_path) as f:
        markdown_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html = markdown_to_html_node(markdown_content).to_html()
    print("\nhtml is:")
    print(html)
    print("-----")

    #title = "<h1>" + extract_title(markdown_content) + "</h1>"
    title = extract_title(markdown_content)
    print(f"title is {title}")

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    # ensure that destination directory exists
    print(f'parent is {dest_path.parent}')
    dest_path.parent.mkdir(parents=True, exist_ok=True)


    with open(dest_path, "w") as f:
        f.write(final_html)