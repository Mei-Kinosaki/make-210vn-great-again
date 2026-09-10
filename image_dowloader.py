from curl_cffi import requests
from bs4 import BeautifulSoup
import os
import json
import logging
logger = logging.getLogger(__name__)

from pathlib import Path
from urllib.parse import urlparse




FORBIDDEN_CHARS = r'\/*?:"<>|'                                              # Khai báo bảng ký tự cấm (thêm \x00-\x1f nếu cần)
trans_table = str.maketrans(FORBIDDEN_CHARS, '-' * len(FORBIDDEN_CHARS))    # Tạo bảng ánh xạ: biến tất cả ký tự cấm thành '-'  
def img_dowloader(link):
    chapter_links = {}
    tags = []
    info = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
        'referer': 'https://www.hentaivnx.live/',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Brave";v="152"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }

    try:
        # Sử dụng curl_cffi với giả lập TLS Vân tay Chrome
        response = requests.get(link, headers=headers, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            h1_tag = soup.select_one('h1')
            name = h1_tag.text.strip().translate(trans_table).strip(' .')
            cover_tag = soup.select_one('div.col-xs-4.col-image > img')
            if cover_tag:
                cover_img = cover_tag.get('src') or cover_tag.get('href') or cover_tag.get('data-src')
            else:
                cover_img = None

            modified_time_tag = soup.select_one('#item-detail > time')
            modified_time = modified_time_tag.text.strip() if modified_time_tag else ""

            list_tags = soup.select('p.col-xs-8 > a')
            for tag in list_tags:
                tags.append(tag.text.strip())

            info.update({'modified_time': modified_time, 'tags': tags})
            relpath_name = os.path.join('database', f'{name}')
            os.makedirs(relpath_name, exist_ok=True)

            with open(os.path.join(relpath_name, 'info.json'), 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=4)

            # Tải ảnh bìa
            if cover_img:
                ext1 = os.path.splitext(cover_img)[1] or '.webp'
                img_res = requests.get(cover_img, headers=headers, impersonate="chrome120", timeout=10)
                if img_res.status_code == 200:
                    filename = os.path.join(relpath_name, f'{name}{ext1}')
                    with open(filename, 'wb') as f:
                        f.write(img_res.content)

            # 3. LẤY DANH SÁCH CHAPTER
            chapters = soup.select('div.col-xs-5.chapter > a')
            for chapter in chapters:
                chap_href = chapter.get('href')
                if chap_href:
                    chapter_links[chap_href] = chapter.text.translate(trans_table).strip(' .')

            # 4. TẢI TỪNG CHAPTER
            for chapter_link, chap_title in chapter_links.items():
                relpath_chap = os.path.join(relpath_name, chap_title)
                
                if not os.path.isdir(relpath_chap):
                    try:
                        chap_res = requests.get(chapter_link, headers=headers, impersonate="chrome120", timeout=15)
                        if chap_res.status_code == 200:
                            chap_soup = BeautifulSoup(chap_res.content, 'lxml')
                            os.makedirs(relpath_chap, exist_ok=True)

                            img_urls = chap_soup.select('div.page-chapter > img')
                            for img_url in img_urls:
                                src = img_url.get('src')
                                if not src:
                                    continue
                                clean_info = list(Path(urlparse(src).path).with_suffix('').parts[1:])  # Bo qua dấu '/' đầu tiên        # p.parent / p.stem sẽ bỏ đuôi file và lấy phần path chuẩn
                                chap_index = clean_info[1] if len(clean_info) > 1 else "0"
                                page_index = clean_info[2] if len(clean_info) > 2 else "0"
                                ext = os.path.splitext(src)[1] or '.webp'
                                page_name = os.path.join(relpath_chap, f'{name}-chap{chap_index}-page{page_index}{ext}')
                                try:
                                    img_data_res = requests.get(src, headers=headers, impersonate="chrome120", timeout=10)
                                    if img_data_res.status_code == 200:
                                        with open(page_name, 'wb') as f:
                                            f.write(img_data_res.content)
                                    else:
                                        print(f"Lỗi Status Code {img_data_res.status_code} khi tải ảnh: {src}")

                                except Exception as e:
                                    print(f"Lỗi tải ảnh đơn lẻ: {e} tại ảnh {page_name}")
                        else:
                            print(f"Lỗi Status Code {chap_res.status_code} tại chap link: {chapter_link}")

                    except Exception as e:
                        logger.exception(f"Lỗi xảy ra khi cào chapter {chapter_link}:")

        else:
            print(f"Lỗi Status Code {response.status_code} tại link truyện: {link}")

    except Exception as e:
        print(f"Lỗi kết nối #1: {e}")