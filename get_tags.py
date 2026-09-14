#li.dropdown.open > ul > li > div > div> ul > li > a
from curl_cffi import requests
from bs4 import BeautifulSoup
import json


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
    all_tags=[]
    response = requests.get(
        f"https://www.hentaivnx.live/tim-truyen",
        headers=headers, 
        impersonate="chrome120"
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        tags= soup.select('li.dropdown > ul > li > div > div> ul > li > a')
        for tag in tags:
            all_tags.append(tag.text.strip())
        with open('tags.json','w',encoding='utf-8') as f:
            json.dump(all_tags,f,ensure_ascii=False,indent=4)
except Exception as e:
    print(e)