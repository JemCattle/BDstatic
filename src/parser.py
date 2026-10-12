from textnode import *
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    split_nodes: list = []
    delimiter_len: int = len(delimiter)
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            split_nodes.append(node)
        else:
            index = 0
            inline = False
            inline_end = 0
            escape_index = []
            for index in range(0, len(node.text)):
                if node.text[index] == delimiter[0]:
                    if index > 0 and node.text[index - 1] == "\\":
                        node.text = node.text[:index-1] + node.text[index:]
                        continue
                    if delimiter_len > 1:
                        if node.text[index:index+delimiter_len] == delimiter:
                            index += delimiter_len - 1
                        else:
                            index += 1
                            continue
                    if not inline:
                        inline_start = index + 1
                        inline = True
                        split_nodes.append(
                            TextNode(node.text[inline_end:inline_start-delimiter_len], TextType.TEXT)
                            )
                    elif inline:
                        inline_end = index - (delimiter_len -1)
                        inline = False
                        split_nodes.append(
                            TextNode(node.text[inline_start:inline_end], text_type)
                            )
                        inline_end += delimiter_len
                index += 1
                if index > len(node.text)-1:
                    break
            if inline:
                raise Exception("unclosed inline block")
            else:
                split_nodes.append(
                            TextNode(node.text[inline_end:index], TextType.TEXT)
                            )
    return split_nodes
# link helper functions
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def helper_link_split_points(image_link: bool, split_points: list, links: list[tuple], text: str) -> list[int]:
    if image_link:
        prefix = 2 # for ! before square bracket
    else:
        prefix = 1
    for alt_text, link in links:
        split_points.append(text.find(alt_text) - prefix)
        split_points.append(text.find(link,split_points[-1]) + len(link) + 1)
    split_points.append(None)
    return split_points

def helper_link_splitter(image_link: bool, node: TextNode, split_points: list[int], new_nodes: list[TextNode], links: list[tuple], count: int = 0) -> list[TextNode]:
    if image_link:
        md_type = TextType.IMAGE
    else:
        md_type = TextType.LINK
    for i in range(0,len(split_points),2):
        if node.text[split_points[i]:split_points[i+1]] != "":
            new_nodes.append(
                TextNode(
                    node.text[split_points[i]:split_points[i+1]],
                            TextType.TEXT)
                    )
        if count < len(links):
            new_nodes.append(
                TextNode(
                    links[count][0],
                    md_type,
                    links[count][1]
                    )
                )
        else:
            continue
        count += 1
    return new_nodes
# split link nodes
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if extract_markdown_images(node.text) == []:
            new_nodes.append(node)
        else:
            image_tuples = extract_markdown_images(node.text)
            split_points = helper_link_split_points(True, [0], image_tuples, node.text)
            image_count = 0
            new_nodes = helper_link_splitter(True, node, split_points, new_nodes, image_tuples, image_count)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
        else:
            link_tuples = extract_markdown_links(node.text)
            split_points = helper_link_split_points(False, [0], link_tuples, node.text)
            link_count = 0
            new_nodes = helper_link_splitter(False, node, split_points, new_nodes, link_tuples, link_count)
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    delimiter_map = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`",
        }
    for txtype in delimiter_map:
        nodes = split_nodes_delimiter(nodes, delimiter_map[txtype], txtype)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
# block parser
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    blocks_for_deletion = []
    for i in range(0, len(blocks)):
        blocks[i] = blocks[i].strip()
        blocks[i] = blocks[i].strip("\n")
        if blocks[i].strip("\n") == "":
            blocks_for_deletion.append(i)
    blocks_for_deletion.reverse()
    for d in blocks_for_deletion:
        del blocks[d]
    return blocks

def block_to_blocktype(block: str) -> BlockType:
    if re.match(r"^#{1,6} ",block):
        return BlockType.HEADING
    if re.match(r"^`{3}\n", block) and re.search(r"\n`{3}$", block):
        return BlockType.CODE
    block_lines = block.split("\n")
    quote = True
    ulist = True
    olist = True
    olist_index = 1
    for line in block_lines:
        check = line[0]
        if not check == ">":
            quote = False
        check = line[0:2]
        if not check == "- ":
            ulist = False
        check = line[0:len(str(olist_index)+". ")]
        if not check == (str(olist_index)+". "):
            olist = False
        olist_index += 1
    if quote:
        return BlockType.QUOTE
    elif ulist:
        return BlockType.UNORDERED_LIST
    elif olist:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
