import requests
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

ext = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
save_dir = "./data"
all_links = list()
visited_urls=set()


def links (a_tags):
    all_links.clear()
    for site in a_tags:
        link=site.get("href")
        if link and link.startswith("http"):
            print(f"references : {link}")
            all_links.append(link)

def download_images(images,url):
    os.makedirs(save_dir, exist_ok=True)
    print(f"\t\nIMAGES FOUIND IN ({url}):")
    for image in images:
        src = image.get("src")
        if src and not src.endswith(tuple(ext)):
            continue
        if src.startswith("//"):
            full_url = "https:" + src
        elif src.startswith("/"):
                full_url = urljoin(url, src)
        elif src.startswith("http"):
                full_url = src
        else:
            full_url = urljoin(url, src)
        try:
            filename = os.path.basename(full_url)
            save_path = os.path.join(save_dir, filename)
            if filename:
                    get_image= requests.get(full_url).content
                    with open(save_path,"wb") as f:
                        f.write(get_image)
                    print(f"Downloaded: {save_path}")
        except Exception as e:
            print("")


def get_headers (url,depth,max_depth,headless):
    if url in visited_urls or depth > max_depth:
        return
    visited_urls.add(url)

    if headless:
        try:
            response = requests.get(url)
            page=BeautifulSoup(response.text,"html.parser")
            print(f"Connection established response:{response} , page converted Successfully...")
            
            img_tags = page.find_all("img")
            download_images(img_tags,url)
            
            if depth < max_depth:
                get_link(url)
                for link in all_links:
                    next_url=link
                    get_headers(next_url,depth+1,max_depth,True)
        except Exception as e:
            print(f"error: {e}")
    else :
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page    = browser.new_page()
                page.goto(url)
                html    = page.content()
                browser.close()
                page = BeautifulSoup(html, "html.parser")
                
                img_tags = page.find_all("img")
                download_images(img_tags,url)
            
            if depth < max_depth:
                get_link(url)
                for link in all_links:
                    next_url=link
                    get_headers(next_url,depth+1,max_depth,False)
        except Exception as e:
            print(f"error: {e}")
            
def get_link (url):
    try:
        response = requests.get(url)
        page=BeautifulSoup(response.text,"html.parser")
        a_tag = page.find_all("a")
        links(a_tag)
    except Exception as e:
        print(f"error: {e}")

def main ():
    parser = argparse.ArgumentParser(description="Recursive image spider")
    parser.add_argument("url", help="Target URL to start crawling")
    parser.add_argument("-r", action="store_true", help="Enable recursive crawling")
    parser.add_argument("-l", type=int, default=5, help="Max recursion depth (default: 5)")
    parser.add_argument("-p", type=str, default="./data", help="Folder path to save images")
    args = parser.parse_args()

    global base_url
    base_url = args.url

    global save_dir
    save_dir=args.p
    get_headers(base_url,0,args.l  if args.r else 0 ,True)
    
    
if __name__ == "__main__":
    main()
   