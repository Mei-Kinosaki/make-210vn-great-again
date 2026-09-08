import requests
import os
api_url = 'https://sv3.2tcdn.cfd/sister-contrast-cuoc-song-ai-an-voi-nhung-nguoi-chi-yeu-chieu/3/3.webp' # API trả về file ảnh trực tiếp

# Dùng stream=True để tải file dung lượng lớn mượt hơn

os.makedirs('downloaded_images',exist_ok=True)
response = requests.get(api_url)
image_urls = response.json().get('message', [])

headers = {'User-Agent': 'Mozilla/5.0'}
if response.status_code == 200:
    with open('downloaded_images/direct_image.jpg', 'wb') as f:
        for idx, url in enumerate(image_urls, 1):
            # Trích xuất đuôi file gốc từ URL (vd: .webp, .png, .jpg)
            ext = os.path.splitext(url)[1] 
            if not ext:  # Nếu URL không có đuôi file thì mặc định gán là .webp
                ext = '.webp'
                
            img_data = requests.get(url, headers=headers).content
            
            filename = f'downloaded_images/image_{idx}{ext}'
            with open(filename, 'wb') as f:
                f.write(img_data)
        
            print(f"Đã tải thành công: {filename}")
    print("Đã tải xong ảnh từ endpoint binary!")
