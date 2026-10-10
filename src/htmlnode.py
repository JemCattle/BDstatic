class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict[str, str] = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string: str = ""
        if self.props is None:
            return prop_string
        for prop in self.props:
            prop_string += " " + prop + "=\"" + self.props[prop] + "\""
        return prop_string

    def __repr__(self):
        return f"HTMLNode(tag=\"{self.tag}\", value=\"{self.value}\", children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: list[HTMLNode] | None, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode must have children (duh)")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            html_tag = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
            return html_tag
