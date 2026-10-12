import unittest
import re
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
                    "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """
# heading

## heading

### heading

#### heading

##### heading

###### heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
                "<div><h1>heading</h1><h2>heading</h2><h3>heading</h3><h4>heading</h4><h5>heading</h5><h6>heading</h6></div>",
        )

    def test_listsblock(self):
        md = """
# ordered list

1. one
2. two
3. red
4. blue
5. five
6. six
7. number nine
8. number nine
9. number nine
10. ten

# unordered list

- hello
- world
- !
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
                "<div><h1>ordered list</h1><ol><li>one</li><li>two</li><li>red</li><li>blue</li><li>five</li><li>six</li><li>number nine</li><li>number nine</li><li>number nine</li><li>ten</li></ol><h1>unordered list</h1><ul><li>hello</li><li>world</li><li>!</li></ul></div>",
        )

    def test_quoteblock(self):
        md = """
> implying this is a quote
>ishygddt
>that feel when no image to html parser
> feelsbadman.jpg
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
                "<div><blockquote>implying this is a quote ishygddt that feel when no image to html parser feelsbadman.jpg</blockquote></div>",
        )

    def test_extract_title(self):
        md = """
# heading
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        self.assertEqual(
            extract_title(md),
                "heading",
        )


    def test_extract_title_2(self):
        md = """
# heading
This is **bolded** paragraph
text in a p
tag here

# another heading

This is another paragraph with _italic_ text and `code` here

"""
        self.assertEqual(
            extract_title(md),
                "heading",
        )


    def test_extract_title_none(self):
        md = """
## heading
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        self.assertRaises(Exception,
            extract_title, md
        )
