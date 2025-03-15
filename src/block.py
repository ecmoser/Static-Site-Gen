from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final = []
    for block in blocks:
        if not block.strip() == '':
            final.append(block.strip())
    return final

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_heading(block):
    is_hashtag = True
    hashtag_count = 0
    while is_hashtag:
        if block[hashtag_count] == "#":
            hashtag_count += 1
            continue
        is_hashtag = False
    if 0 < hashtag_count < 7 and block[hashtag_count] == ' ':
        return True
    return False

def is_code(block):
    return (len(block) > 6 and 
            block[:3] == "```" and 
            block[-3:] == "```")

def is_quote(block):
    for line in block.splitlines():
        if not line[0] == ">":
            return False
    return True

def is_unordered_list(block):
    for line in block.splitlines():
        if not line[:2] == "- ":
            return False
    return True

def is_ordered_list(block):
    number = 1
    for line in block.splitlines():
        if not line[0] == str(number) or not line[1:3] == ". ":
            return False
        number += 1
    return True
