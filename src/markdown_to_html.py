from parser import text_to_textnodes, markdown_to_blocks, block_to_blocktype
from textnode import TextNode, text_node_to_html_node, BlockType, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        tag = blocktype_to_tag(block_type)
        props = None
        match block_type:
            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                lines = block.split("\n")
                if block_type == BlockType.UNORDERED_LIST:
                    delimiter = "-"
                else:
                    delimiter = "."
                line_nodes = []
                for line in lines:
                    line = line[line.find(delimiter)+1:].strip()
                    children = text_to_children(line)
                    line_nodes.append(ParentNode(tag="li", children=children, props=None))
                children = line_nodes
            case BlockType.HEADING:
                tag += str(block.count("#", 0, block.find(" ")+1))
                children = text_to_children(block[block.count("#", 0, block.find(" ")+1)+1:])
            case BlockType.QUOTE:
                lines = block.split("\n")
                clean_lines = []
                for line in lines:
                    line = line[1:]
                    line = line.strip()
                    clean_lines.append(line)
                block = " ".join(clean_lines)
                children = text_to_children(block)
            case BlockType.PARAGRAPH:
                children = text_to_children(block.replace("\n", " "))
            case BlockType.CODE:
                tag = "pre"
                children = [text_node_to_html_node(TextNode(block[4:-3],TextType.CODE))]
        nodes.append(ParentNode(tag,children,props))
    return ParentNode(tag="div", children=nodes)

def text_to_children(text) -> list[LeafNode]:
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
    
def blocktype_to_tag(block_type: BlockType) -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return "h"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
