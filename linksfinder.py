from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import os
FILE_PATH="links_database.json"
def load_existing_links(file_path):
    existing_links=set()
    if os.path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing_links.add(line.strip())
    return existing_links
def prepend_links(file_path,newlinks):
    temp_file=file_path + '.tmp'
    with open (temp_file, "w",encoding="utf-8") as f:
        if not newlinks:
            print("There is not any new links")
            return
        for link in newlinks:
            f.write(link)
        with open(file_path,"r",encoding="utf-8") as old_f:
            for line in old_f:
                f.write(line)
    os.replace(temp_file,file_path)
    return
def get_links():
    existing_links=load_existing_links(FILE_PATH)
    is_first_run=len(existing_links)==0
    stop_scraping=False
    current_page = 1
    newlinks=[]
    while not stop_scraping:
        # Giả lập chính xác Request Headers bạn vừa gửi
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="152", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
        }
        # Giả lập vân tay TLS Chrome vượt Cloudflare WAF
        response = requests.get(
            f"https://www.hentaivnx.live/{current_page}", 
            headers=headers, 
            impersonate="chrome120"
        )
        #Tim trang cuoi cung
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            if is_first_run():
                all_page= soup.select("a.page-link")
                last_page_number=all_page[-2].text.strip()
            links=soup.select("a.jtip")["href"]
            for link in links:
                if link not in newlinks:
                    newlinks.append(link)
                else:
                    stop_scraping=True
                    break
        prepend_links(FILE_PATH,newlinks)
        current_page+=1
        if current_page == last_page_number:
            stop_scraping=True