from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        split_node = node.text.split(delimiter)
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue
        if not node.text.count(delimiter) % 2 == 0:
            raise Exception("No closing delimiter found")
        if node.text.find(delimiter) == 0:
            type = text_type
        else:
            type = node.text_type
        for part in split_node:
            if not part == '':
                new_nodes.append(TextNode(part, type))
                type = text_type if type == node.text_type else node.text_type
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    final = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            final.append(node)
            continue
        final_node = []
        images = extract_markdown_images(node.text)
        image_pattern = r"!\[.*?\]\(.*?\)"
        text_parts = re.split(image_pattern, node.text)
        text_type = TextType.TEXT
        part_index = 0
        while part_index < len(text_parts):
            if text_type == TextType.TEXT:
                if not text_parts[part_index] == '':
                    final_node.append(TextNode(text_parts[part_index], TextType.TEXT))
                text_type = TextType.IMAGE
                continue
            elif part_index < len(images):
                final_node.append(TextNode(images[part_index][0], TextType.IMAGE, images[part_index][1]))
            text_type = TextType.TEXT
            part_index += 1
        final += final_node
    return final

def split_nodes_link(old_nodes):
    final = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            final.append(node)
            continue
        final_node = []
        links = extract_markdown_links(node.text)
        links_pattern = r"\[.*?\]\(.*?\)"
        text_parts = re.split(links_pattern, node.text)
        text_type = TextType.TEXT
        part_index = 0
        while part_index < len(text_parts):
            if text_type == TextType.TEXT:
                if not text_parts[part_index] == '':
                    final_node.append(TextNode(text_parts[part_index], TextType.TEXT))
                text_type = TextType.LINK
                continue
            elif part_index < len(links):
                final_node.append(TextNode(links[part_index][0], TextType.LINK, links[part_index][1]))
            text_type = TextType.TEXT
            part_index += 1
        final += final_node
    return final

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes