import os
from linksfinder import get_links
from image_dowloader import img_dowloader
import logging
from datetime import datetime

os.makedirs('logs', exist_ok=True)
log_filename = os.path.join('logs', f"error_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(        # Cấu hình logging toàn hệ thống
    filename=log_filename,
    filemode='a',           # 'a' = Append (ghi nối tiếp các lần chạy trong ngày, không ghi đè)
    format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.ERROR,
    encoding='utf-8'
)

def main():
    os.makedirs('database',exist_ok=True)    
    links_to_update=get_links()
    for link in links_to_update:
        try:
            img_dowloader(link)
        except Exception as e:
            print(f'Đã xảy ra lỗi khi tải {link}:',e)

if __name__ == "__main__":
    print("Đang chạy main.py...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Đã hủy chương trình bằng Ctrl + C.")