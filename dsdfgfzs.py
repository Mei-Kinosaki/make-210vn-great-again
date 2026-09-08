import requests
import os

img_url = "https://sv3.2tcdn.cfd/sister-contrast-cuoc-song-ai-an-voi-nhung-nguoi-chi-yeu-chieu/3/4.webp"

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

os.makedirs('downloaded_images', exist_ok=True)

try:

    response = requests.get(img_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        with open('downloaded_images/2.webp', 'wb') as f:
            f.write(response.content)
        print("Tải ảnh .webp thành công!")
    else:
        print(f"Lỗi Status Code: {response.status_code}")

except Exception as e:
    print(f"Lỗi kết nối: {e}")