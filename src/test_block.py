import unittest
from block import *

class Test_Block_Functions(unittest.TestCase):
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
    
    def test_markdown_to_block_empty_leading_and_following(self):
        md = ("""

1
2

3

4
5
6


            """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1\n2", "3", "4\n5\n6"])


    def test_block_to_block_type_code(self):
        block = "```Hello this is code \n more code stuff```"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.CODE)

    def test_block_to_block_type_heading(self):
        block = "#### This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_block_type_quote(self):
        block = "> Hello \n> There \n> World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Hello \n- There \n- World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_list(self):
        block = "1. Hello \n2. There \n3. World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_wrong_order_list(self):
        block = "1. Hello\n 3. World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_unordered_list(self):
        block = "-Hello\n- World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_quote(self):
        block = "> Hello \n > World"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_heading(self):
        block = "####### This isn't a heading"
        block2 = "#Also not a heading"
        type = block_to_block_type(block)
        type2 = block_to_block_type(block2)
        self.assertEqual(type, BlockType.PARAGRAPH)
        self.assertEqual(type2, BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_code(self):
        block = "`` THis isn't code ```"
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)