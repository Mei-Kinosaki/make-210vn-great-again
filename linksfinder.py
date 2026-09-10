from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import os
import logging
logger = logging.getLogger(__name__)
FILE_PATH="links_database.json"     

def load_existing_links(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    except Exception:
        pass
        
    return {}

def get_links():
    existing_links=load_existing_links(FILE_PATH)
    stop_scraping=False
    current_page = 1
    newlinks={}

    while not stop_scraping:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
            'referer': 'https://www.hentaivnx.live/',
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.7',
            'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Brave";v="152"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site'
        }
        # Giả lập vân tay TLS Chrome vượt Cloudflare WAF
        try:
            response = requests.get(
                f"https://www.hentaivnx.live/?page={current_page}",       #https://www.hentaivnx.live/?page=47
                headers=headers, 
                impersonate="chrome120"
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                all_page= soup.select("a.page-link")
                last_page_number=int(all_page[-2].text.strip())        #Tim trang cuoi cung (gan 2000 trang)
                items = soup.select("figure")
                page_has_duplicate=False
                page_new_count = 0
                for item in items:
                    link_tag = item.select_one("a.jtip")
                    update_tag = item.select_one("figcaption > ul > li:nth-child(1) > a")
                    
                    if not link_tag or not update_tag:
                        continue
                    link = link_tag.get("href")
                    update = update_tag.text.strip()
                    if not link:
                        continue
                    if existing_links.get(link) != update:
                        if link not in newlinks:
                            newlinks[link] = update
                            page_new_count += 1
                    else:
                        page_has_duplicate = True
                print(f"Đã duyệt xong trang {current_page}: +{page_new_count} link mới (Tổng gom được: {len(newlinks)})")
                current_page+=1
                if page_has_duplicate:
                    print("--> Đã đụng dữ liệu cũ. Dừng tìm kiếm link mới!")
                    stop_scraping = True
                    break
                if current_page >= last_page_number:
                    stop_scraping=True
            else:
                print(f"Lỗi Status Code: {response.status_code} tại page {current_page}")
                break
        except Exception as e:
            # logger.exception sẽ tự động ghi lại toàn bộ Traceback lỗi
            logger.exception("Lỗi xảy ra trong hàm get_links():")
    if newlinks:
        existing_links.update(newlinks)
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_links, f, ensure_ascii=False, indent=4)
        print(f"==> Đã lưu {len(newlinks)} link mới vào {FILE_PATH}")
    return newlinks
