from textnode import TextType, TextNode
from markdown_to_html import markdown_to_html_node, extract_title
import os
import time
import shutil

def main():
    log = []
    copy_static(log, "./static/" , "./public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as p:
        page = p.read()
    with open(template_path) as t:
        template = t.read()
    html = markdown_to_html_node(page).to_html()
    title = extract_title(page)
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w+') as d:
        d.write(new_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    for item in content:
        if os.path.isdir(os.path.join(dir_path_content, item)):
            generate_pages_recursive(os.path.join(dir_path_content, item),template_path, os.path.join(dest_dir_path, item))
        else:
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item.replace(".md", ".html")))

def log_format(path: str, action: str, target: str | None) -> dict:
    return {
        "timecode": time.gmtime(),
        "path": path,
        "action": action,
        "target": target
        }

def log_print(log_dict):
    print(
        " ".join([
                time.strftime("%Y-%m-%d %H:%M:%S", log_dict["timecode"]),
                log_dict["path"],
                log_dict["action"],
                log_dict["target"]]
            )
        )

def copy_to_public(log: list[dict], static_path: str, public_path: str) -> None:
    dir_list = os.listdir(static_path)
    for item in dir_list:
        item_path = os.path.join(static_path, item)
        if os.path.isfile(item_path):
            log_entry = log_format(item_path, "copy to",  shutil.copy(item_path, os.path.join(public_path, item)))
            log_print(log_entry)
            log.append(log_entry)
        else:
            os.mkdir(os.path.join(public_path, item))
            copy_to_public(log, item_path, os.path.join(public_path, item))

def copy_static(log: list[dict], static_path: str, public_path: str) -> None:
    if not os.path.exists(static_path):
        raise Exception("static path does not exist")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    copy_to_public(log, static_path, public_path)

main()
