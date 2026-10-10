from textnode import TextType, TextNode
import os
import time
import shutil

def main():
    log = []
    copy_static(log, "./static/" , "./public/")
    # print(log)
    

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
