from textnode import *
from parser import *


test_text = "This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev)."
nodes = text_to_textnodes(test_text)
print("\n")
print(nodes)
