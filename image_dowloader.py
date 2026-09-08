import requests
import os
from bs4 import BeautifulSoup

def img_dowloader(link):
    link="https://abc.xyz"
    name=link.split(r'//')[1].split('.')[0]
    os.makedirs('name')
    chapter_links=[]
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
    try:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code==200:
            soup=BeautifulSoup(response,'html.parser')
            chapters=soup.selector('a.')        #sửa lại
            for chapter in chapters:
                chapter_links.append(chapter['href'])
        else:
            print(f"Lỗi Status Code: {response.status_code}")
    except Exception as e:
            print(f"Lỗi kết nối: {e}")
    for chapter_link in chapter_links:
        try:
            response = requests.get(chapter_link, headers=headers, timeout=10)
            if response.status_code==200:
                soup=BeautifulSoup(response,'html.parser')
                os.makedirs(f'{soup.select_one('div')}')        #sửa lại
                img_urls=soup.select('a.')              #sửa lại
                for img_url in img_urls:
                    try:
                        chap_index=img_url.get_text()       #sửa lại
                        page_index=img_url.get_text()       #sửa lại
                        response = requests.get(img_url['href'], headers=headers, timeout=10)
                        if response.status_code == 200:     #tải file binary
                            with open(f'{name} chap {chap_index} page {page_index}.webp', 'wb') as f:
                                f.write(response.content)
                        else:
                            print(f"Lỗi Status Code: {response.status_code} tại ảnh chap {chap_index} page {page_index}")
            
                    except Exception as e:
                        print(f"Lỗi kết nối: {e}")
            else:
                print(f"Lỗi Status Code: {response.status_code}")
        except Exception as e:
                print(f"Lỗi kết nối: {e}")
        