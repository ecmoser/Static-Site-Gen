import unittest
from textnode import TextNode, TextType
from inline import *

class TestInline(unittest.TestCase):
    def test_normal_case(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_start_of_string(self):
        node = TextNode("**Bold** is my new favorite style", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Bold", TextType.BOLD),
                                     TextNode(" is my new favorite style", TextType.TEXT)])
    
    def test_end_of_string(self):
        node = TextNode("I love to `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("I love to ", TextType.TEXT),
                                     TextNode("code", TextType.CODE)])
        
    def test_multiple_occurences(self):
        node = TextNode("I like **bold** words but I also like **BOLD** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("I like ", TextType.TEXT),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" words but I also like ", TextType.TEXT),
                                     TextNode("BOLD", TextType.BOLD),
                                     TextNode(" words", TextType.TEXT)])
        
    def test_multple_nodes(self):
        node1 = TextNode("This is the _first_ node", TextType.TEXT)
        node2 = TextNode("This is the _second_ node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is the ", TextType.TEXT),
                                     TextNode("first", TextType.ITALIC),
                                     TextNode(" node", TextType.TEXT),
                                     TextNode("This is the ", TextType.TEXT),
                                     TextNode("second", TextType.ITALIC),
                                     TextNode(" node", TextType.TEXT)])

    def test_illegal_markdown(self):
        node = TextNode("This is an _illegal itallic", TextType.TEXT)
        self.assertRaises(Exception, lambda: split_nodes_delimiter([node], "_", TextType.ITALIC))

    def test_wrong_test_type(self):
        node = TextNode("This is the wrong type", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is the wrong type", TextType.CODE)])

    def test_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(matches, expected)
    
    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, expected)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_image_split_nodes(self):
        node = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT
        )]
        split_nodes = split_nodes_image(node)
        expected_nodes = [TextNode("This is text with an ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                          TextNode(" and another ", TextType.TEXT),
                          TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_image_split_nodes_leading(self):
        node = [TextNode("![leading image](https://google.com) is in front of this text", TextType.TEXT)]
        split_nodes = split_nodes_image(node)
        expected_nodes = [TextNode("leading image", TextType.IMAGE, "https://google.com"),
                          TextNode(" is in front of this text", TextType.TEXT)]
        self.assertEqual(split_nodes, expected_nodes)

    def test_image_split_nodes_trailing(self):
        node = [TextNode("The image is behind this text ![trailing image](https://google.com)", TextType.TEXT)]
        split_nodes = split_nodes_image(node)
        expected_nodes = [TextNode("The image is behind this text ", TextType.TEXT),
                          TextNode("trailing image", TextType.IMAGE, "https://google.com")]
        self.assertEqual(split_nodes, expected_nodes)   

    def test_image_split_nodes_back_to_back(self):
        node = [TextNode("These images are ![first image](foo.bar)![second image](https://google.com) back to back", TextType.TEXT)]
        split_nodes = split_nodes_image(node)
        expected_nodes = [TextNode("These images are ", TextType.TEXT),
                          TextNode("first image", TextType.IMAGE, "foo.bar"),
                          TextNode("second image", TextType.IMAGE, "https://google.com"),
                          TextNode(" back to back", TextType.TEXT)]
        self.assertEqual(split_nodes, expected_nodes)

    def test_image_split_nodes_multiple(self):
        nodes = [TextNode("This is the first node ![first image](foo.bar)", TextType.TEXT),
                 TextNode("And this is the second ![second image](https://google.com)", TextType.TEXT)]
        split_nodes = split_nodes_image(nodes)
        expected_nodes = [TextNode("This is the first node ", TextType.TEXT),
                          TextNode("first image", TextType.IMAGE, "foo.bar"),
                          TextNode("And this is the second ", TextType.TEXT),
                          TextNode("second image", TextType.IMAGE, "https://google.com")]
        self.assertEqual(split_nodes, expected_nodes)
        
    def test_link_split_nodes(self):
        node = [TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT
        )]
        split_nodes = split_nodes_link(node)
        expected_nodes = [TextNode("This is text with an ", TextType.TEXT),
                          TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                          TextNode(" and another ", TextType.TEXT),
                          TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_link_split_nodes_leading(self):
        node = [TextNode("[leading link](https://google.com) is in front of this text", TextType.TEXT)]
        split_nodes = split_nodes_link(node)
        expected_nodes = [TextNode("leading link", TextType.LINK, "https://google.com"),
                          TextNode(" is in front of this text", TextType.TEXT)]
        self.assertEqual(split_nodes, expected_nodes)

    def test_link_split_nodes_trailing(self):
        node = [TextNode("The link is behind this text [trailing link](https://google.com)", TextType.TEXT)]
        split_nodes = split_nodes_link(node)
        expected_nodes = [TextNode("The link is behind this text ", TextType.TEXT),
                          TextNode("trailing link", TextType.LINK, "https://google.com")]
        self.assertEqual(split_nodes, expected_nodes)   

    def test_link_split_nodes_back_to_back(self):
        node = [TextNode("These links are [first link](foo.bar)[second link](https://google.com) back to back", TextType.TEXT)]
        split_nodes = split_nodes_link(node)
        expected_nodes = [TextNode("These links are ", TextType.TEXT),
                          TextNode("first link", TextType.LINK, "foo.bar"),
                          TextNode("second link", TextType.LINK, "https://google.com"),
                          TextNode(" back to back", TextType.TEXT)]
        self.assertEqual(split_nodes, expected_nodes)

    def test_link_split_nodes_multiple(self):
        nodes = [TextNode("This is the first node [first link](foo.bar)", TextType.TEXT),
                 TextNode("And this is the second [second link](https://google.com)", TextType.TEXT)]
        split_nodes = split_nodes_link(nodes)
        expected_nodes = [TextNode("This is the first node ", TextType.TEXT),
                          TextNode("first link", TextType.LINK, "foo.bar"),
                          TextNode("And this is the second ", TextType.TEXT),
                          TextNode("second link", TextType.LINK, "https://google.com")]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertEqual(nodes, [
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
                                ])