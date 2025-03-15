import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
   
   def test_print(self):
      node = HTMLNode("h1", "This is a HTML Node", [], {})
      self.assertEqual(str(node), 'HTMLNode(h1, This is a HTML Node, [], {})')

   def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

   def test_lead_to_html_with_url(self):
      node = LeafNode("a", "Hello, world!", {"href":"https://google.com"})
      self.assertEqual(node.to_html(), '<a href="https://google.com">Hello, world!</a>')
      
   def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
 
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