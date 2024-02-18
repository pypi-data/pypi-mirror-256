import requests
import re

def find_img_path(md: str) -> list:
    img_urls_md = re.findall(r"!\[.*?\]\((.*?)\)", md)
    img_urls_html = re.findall(r"<img.*?src=\"(.*?)\".*?>", md)
    return img_urls_md + img_urls_html

def img_path_is_url(img_path: str) -> bool:
    return bool(re.match(r"http?://", img_path))

def download_img(img_path: str, output: str) -> None:
    r = requests.get(img_path)
    img_name = img_path.split('/')[-1]

    if r.status_code == 200:
        with open(f"{output}/{img_name}", 'wb') as f:
            f.write(r.content)
        print(f"🔥 Downloaded {img_path} to {output}/{img_name}")
    
    else:
        print(f"💀 Failed to download {img_path} with status code {r.status_code}")


