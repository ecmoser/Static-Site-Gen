class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ''
        for key in self.props:
            html += f' {key}={self.props[key]}'
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leafs must have a value")
        if self.tag == None:
            return self.value
        html = f"<" + self.tag
        if not self.props is None:
            for key in self.props:
                html += " " + key + '="' + self.props[key] + '"'
        html += ">" + self.value + f"</{self.tag}>"
        return html
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have at least one child")
        html = "<" + self.tag + ">"
        for child in self.children:
            html += child.to_html()
        html += "</" + self.tag + ">"
        return html
    