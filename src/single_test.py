from textnode import *
from parser import *



block = """1. this is an ordered list block
2. every line starts with an ordinal number
3. there must be a full stop and space afterwards
4. this is mandatory
5. the number increments by 1 each line
6. a
7. a
8. a
9. a
10. a
11. there can be empty items in the list"""
print(BlockType.ORDERED_LIST == block_to_blocktype(block))
