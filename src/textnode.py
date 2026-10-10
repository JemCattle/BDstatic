from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        if (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
            ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

class BlockType(Enum):
    PARAGRAPH = "untyped block"
    HEADING = "Headings start with 1-6 # characters, followed by a space and then the heading text."
    CODE = "Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks."
    QUOTE = "Every line in a quote block must start with a \"greater-than\" character: > followed by the quote text. A space after > is allowed but not required."
    UNORDERED_LIST = "Every line in an unordered list block must start with a - character, followed by a space."
    ORDERED_LIST = "Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line."
