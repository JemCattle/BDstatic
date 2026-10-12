import unittest
import re
from textnode import *
from parser import *


class TestSplitNodes(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])


    def test_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_wrong_bold(self):
        node = TextNode("This is text with a *bold block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a *bold block* word", TextType.TEXT)
        ])

    def test_escaped_bold(self):
        node = TextNode(r"This is text with a \**bold block\** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a **bold block** word", TextType.TEXT)
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
# image split tests
    def test_split_images(self):
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
            )

    def test_split_images_no_image(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a **bold block** word", TextType.TEXT)
        ])

    def test_split_images_just_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
            )

    def test_split_images_just_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
            )
# link split tests
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                ],
            new_nodes,
            )

    def test_split_links_no_link(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a **bold block** word", TextType.TEXT)
        ])

    def test_split_links_just_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
            )

    def test_split_links_just_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
            )
# test markdown to TextNodes function
    def test_text_to_textnodes(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
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
            ],
            nodes,
            )
            
    def test_links_to_textnodes(self):
        test_text = "This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev)."
        nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode("This site was generated with a custom-built ", TextType.TEXT),
                TextNode("static site generator", TextType.LINK, "https://www.boot.dev/courses/build-static-site-generator-python"),
                TextNode(" from the course on ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
            )
# test blocks
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

    def test_markdown_to_blocks_blank_lines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

hello








- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "hello",
                "- This is a list\n- with items",
            ],
        )
    def test_headings(self):
        h1 = "# heading 1"
        h2 = "## heading 2"
        h3 = "### heading 3"
        h4 = "#### heading 4"
        h5 = "##### heading 5"
        h6 = "###### heading 6"
        headings = [h1, h2, h3, h4, h5, h6]
        for heading in headings:
            self.assertEqual(BlockType.HEADING, block_to_blocktype(heading))

    def test_code_block(self):
        block = """```
this is a code block
print("hello world!")
```"""
        self.assertEqual(BlockType.CODE, block_to_blocktype(block))

    def test_quote_block(self):
        block = """>this is a quote block
>every line starts with a greater than sign
> there can be a space afterwards
>but this is not mandatory"""
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(block))

    def test_not_quote_block(self):
        block = """>this is a quote block
>every line starts with a greater than sign
 there can be a space afterwards
>but this is not mandatory"""
        self.assertNotEqual(BlockType.QUOTE, block_to_blocktype(block))

    def test_ulist_block(self):
        block = """- this is a list block
- every line starts with a dash
- there must be a space afterwards
- this is mandatory"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(block))

    def test_not_ulist_block(self):
        block = """- this is a list block
- every line starts with a dash
-there must be a space afterwards
- this is mandatory"""
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_blocktype(block))

    def test_olist_block(self):
        block = """1. this is an ordered list block
2. every line starts with an ordinal number
3. there must be a full stop and space afterwards
4. this is mandatory
5. the number increments by 1 each line
6. 
7. 
8. 
9. 
10. 
11. there can be empty items in the list"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(block))
        
    def test_not_olist_block(self):
        block = """1. this is an ordered list block
2. every line starts with an ordinal number
3. there must be a full stop and space afterwards
4. this is mandatory
5. the number increments by 1 each line
5. 
7. 
8. 
9. 
10. 
11. there can be empty items in the list"""
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_blocktype(block))

    def test_paragraph_block(self):
        block = """This is just a regular paragraph
with line breaks
but not double line breaks.
This is **bolded** text.
This is a line with _italic_ text and `code` here.
This is more text."""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))
