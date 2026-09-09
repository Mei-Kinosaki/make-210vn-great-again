import requests
import os
from bs4 import BeautifulSoup
import logging
import json

logger = logging.getLogger(__name__)
FORBIDDEN_CHARS = r'\/*?:"<>|'                                              # Khai báo bảng ký tự cấm (thêm \x00-\x1f nếu cần)
trans_table = str.maketrans(FORBIDDEN_CHARS, '-' * len(FORBIDDEN_CHARS))    # Tạo bảng ánh xạ: biến tất cả ký tự cấm thành '-'

def img_dowloader(link):    #link(str)
    chapter_links={}
    tags=[]
    info={}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
        'referer': 'https://placeholder/',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Brave";v="152"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site'
    }
    try:
        response = requests.get(link, headers=headers, timeout=10)         #vao link truyen
        if response.status_code==200:
            soup=BeautifulSoup(response.content,'lxml')
            name=soup.select_one('h1').text
            name = name.translate(trans_table)                             # 1. Thay thế các ký tự bị cấm trên Windows/Linux/Mac thành dấu gạch ngang '-'  # Cấm: \ / : * ? " < > | và các ký tự điều khiển ASCII (0-31)          
            name = name.strip(' .')                                        # 2. Xóa các khoảng trắng thừa hoặc khoảng trắng/dấu chấm ở đầu và cuối tên file

            cover_img=soup.select_one('div.col-xs-4.col-image > img')['href']
            modified_time=soup.select_one('#item-detail > time').text
            list_tags=soup.select(' p.col-xs-8 > a')
            for tag in list_tags:
                tags.append(tag.text)
            info.update({'modified_time':modified_time,'tags':tags})       #sap xep theo ngay update hoac tags
            relpath_name=os.path.join('database',f'{name}')
            os.makedirs(relpath_name,exist_ok=True)
            with open(f'{relpath_name}/info.json','w',encoding='utf-8') as f:
                json.dump(info,f,ensure_ascii=False,indent=4)
            ext1 = os.path.splitext(cover_img)[1]                           # Trích xuất đuôi file gốc từ img (vd: .webp, .png, .jpg)
            if not ext1:                                                    # Nếu img không có đuôi file thì mặc định gán là .webp
                ext1 = '.webp'
            img_data = requests.get(cover_img, headers=headers).content                     #                  
            filename = f'{name}{ext1}'
            filename= os.path.join(relpath_name,filename)
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            chapters=soup.select('div.col-xs-5.chapter > a')        
            for chapter in chapters:
                chapter_links[chapter['href']]=chapter.text.translate(trans_table).strip(' .')
            for chapter_link in chapter_links:
                    relpath_chap=os.path.join(relpath_name,chapter_links[chapter_link])           #- Chapter 3 hoac - OneShot
                    if not os.path.isdir(relpath_chap):                                             #kiem tra chap moi can update
                        try:

                            response = requests.get(chapter_link, headers=headers, timeout=10)      #vao link chap
                            if response.status_code==200:
                                soup=BeautifulSoup(response.content,'lxml')
                                os.makedirs(relpath_chap)
                                img_urls=soup.select('img')
                                for img_url in img_urls:
                                    try:

                                        clean_info=img_url['src'].replace('https://sv3.2tcdn.cfd/','').replace('.webp','').split('/')  #src="https://sv3.2tcdn.cfd/cai-gi-do-khong-nen-biet/0/1.webp"
                                        chap_index=clean_info[1]
                                        page_index=clean_info[2]
                                        response = requests.get(img_url['src'], headers=headers, timeout=10)
                                        ext = os.path.splitext(img_url['src'])[1]                          # Trích xuất đuôi file gốc từ img (vd: .webp, .png, .jpg)
                                        if not ext:                                                 # Nếu img không có đuôi file thì mặc định gán là .webp
                                            ext = '.webp'
                                        if response.status_code == 200:                             #tải file binary
                                            img_data=response.content
                                            page_name=f'{name}-chap{chap_index}-page{page_index}{ext}'
                                            page_name=os.path.join(relpath_chap,page_name)
                                            with open(page_name, 'wb') as f:
                                                f.write(img_data)

                                        else:
                                            print(f"Lỗi Status Code: {response.status_code} tại truyện {name} chap {chap_index} ảnh page {page_index}")    
                                    except Exception as e:
                                        print(f"Lỗi kết nối: {e}")
                                        logger.exception("Lỗi xảy ra trong hàm img_dowload():")     # logger.exception sẽ tự động ghi lại toàn bộ Traceback lỗi
                            else:
                                print(f"Lỗi Status Code: {response.status_code}")
                        except Exception as e:
                            logger.exception("Lỗi xảy ra trong hàm img_dowload():")                 # logger.exception sẽ tự động ghi lại toàn bộ Traceback lỗi
        else:
            print(f"Lỗi Status Code: {response.status_code}")
    except Exception as e:
            print(f"Lỗi kết nối: {e}")
    