from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
from inline import *
import os, shutil

def from_source_to_destination(source, destination):
        if not os.path.exists(source):
                raise Exception(f"{source} path does not exist")
        if os.path.isfile(source):
                shutil.copy(source, destination)
                return
        if os.path.exists(destination):
                shutil.rmtree(destination)
        os.mkdir(destination)
        for child in os.listdir(source):
                from_source_to_destination(os.path.join(source, child), os.path.join(destination, child))

def generate_path(from_path, template_path, dest_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        with open(from_path) as f:
                md = f.read()
                f.close()
        with open(template_path) as f:
                template = f.read()
                f.close()
        node = markdown_to_html_node(md)
        html = node.to_html()
        title = extract_title(md)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", md)
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)
        with open(dest_path, "w") as write_file:
                write_file.write(html)
        write_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
        for content in os.listdir(dir_path_content):
                if not os.path.exists(dir_path_content):
                        raise Exception(f"{dir_path_content} content path does not exist")
                if not os.path.exists(dest_dir_path):
                        raise Exception(f"{dest_dir_path} destination path does not exist")
                content_path = os.path.join(dir_path_content, content)
                destination_path = os.path.join(dest_dir_path, content).replace("md", "html")
                if os.path.isfile(content_path):
                        generate_path(content_path, template_path, destination_path)
                else:
                        os.makedirs(content_path, exist_ok=True)
                        generate_pages_recursive(content_path, template_path, destination_path)

def main():
        shutil.rmtree("public")
        os.mkdir("public")
        from_source_to_destination("static", "public")
        generate_pages_recursive("content", "template.html", "public")
        
main()