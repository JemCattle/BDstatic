import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_data(self):
        node_link = HTMLNode(value="backend", tag="a", props={"href": "https://www.boot.dev"})
        node_heading = HTMLNode(value="Front-end Development is the Worst", tag="h1")
        node_body = HTMLNode(tag="body", children=[node_heading, node_link])
        self.assertEqual(str(node_link), "HTMLNode(tag=\"a\", value=\"backend\", children=None, props={\'href\': \'https://www.boot.dev\'})")

    def test_blank(self):
        blank_node = HTMLNode()
        self.assertEqual(blank_node.tag, None)
        self.assertEqual(blank_node.value, None)
        self.assertEqual(blank_node.children, None)
        self.assertEqual(blank_node.props, None)

    def test_props_to_html(self):
        node_link = HTMLNode(value="backend", tag="a", props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node_link.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")

class TestLeafNode(unittest.TestCase):
    def test_data(self):
        node_link = LeafNode(value="backend", tag="a", props={"href": "https://www.boot.dev"})
        node_heading = LeafNode(value="Front-end Development is the Worst", tag="h1")
        #node_body = LeafNode(tag="body", children=[node_heading, node_link])
        #print("testing leaf node data\nlink:")
        #print(node_link)
        #print("heading:")
        #print(node_heading)

    def test_node_to_html(self):
        node_link = LeafNode(value="backend", tag="a", props={"href": "https://www.boot.dev", "target": "_blank"})
        node_none_tag = LeafNode(tag=None, value="Front-end Development is the Worst")
        self.assertEqual(node_link.to_html(), "<a href=\"https://www.boot.dev\" target=\"_blank\">backend</a>")
        self.assertEqual(node_none_tag.to_html(), node_none_tag.value)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        child_node1 = LeafNode("h1", "child1")
        child_node2 = LeafNode("h2", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><h1>child1</h1><h2>child2</h2></div>")

if __name__ == "__main__":
    unittest.main()
