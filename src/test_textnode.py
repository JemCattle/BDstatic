import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_blank_url(self):
        url_empty_test = TextNode("this is not a link", TextType.TEXT)
        self.assertEqual(url_empty_test.url, None)

    def test_explicit_blank_url(self):
        url_explicit_none = TextNode("this has no URL", TextType.BOLD, None)
        self.assertEqual(url_explicit_none.url, None)

    def test_uneq(self):
        node = TextNode("This is an ITALIC text node", TextType.ITALIC)
        node2 = TextNode("This is a BOLD text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_partial_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Is this a text node?", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        link_node = TextNode("backend", TextType.LINK, url="https://www.boot.dev")
        html_link = text_node_to_html_node(link_node)
        self.assertEqual(html_link.to_html(), "<a href=\"https://www.boot.dev\">backend</a>")

    def test_image(self):
        image_node = TextNode("backend", TextType.IMAGE, url="https://www.boot.dev")
        html_image = text_node_to_html_node(image_node)
        self.assertEqual(html_image.to_html(), "<img src=\"https://www.boot.dev\" alt=\"backend\"></img>")

if __name__ == "__main__":
    unittest.main()
