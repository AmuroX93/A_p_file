import os
import requests
from bs4 import BeautifulSoup,NavigableString
from urllib.parse import urljoin, urlparse

def download_images_from_url(url, start_page, end_page ,save_folder):
    """
    从指定 URL 获取所有图片并保存到文件夹。
    """
    
    # 1. 创建存储文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"已创建文件夹: {save_folder}")

    # 2. 设置请求头,cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'cookie':'_gid=GA1.2.1746754044.1764575270; _ga=GA1.1.679134168.1764245852; _ga_D0KMFL0GNL=GS2.1.s1764588153$o3$g0$t1764588153$j60$l0$h0;\
              XSRF-TOKEN=eyJpdiI6IkdNZDNwWG5PY1VsTWxhUEtzSGZveHc9PSIsInZhbHVlIjoid1NEMUwySVlXbG9RRWFBaWNjZlplN2I0MWZIOU53ckFrYU1DT3VcL2FNaFd4TEU1eE5\
                uK3NiSGZLSWkyMXJTSmhDVEozMjI1K0tIUE9tSGZSWjQ5YmxRPT0iLCJtYWMiOiIzODMwZmJjZWY3ZjEwZDZlM2FkMTA5Y2Y0NzU2ZDM1ZjVlYjJiMGRlZGI3MTQ0YjcwZGVl\
                    YjViMzM4OGFkYTQwIn0%3D; _session=eyJpdiI6IlFzcEk0R2FYUjhSZ0hmM2t5emsyNkE9PSIsInZhbHVlIjoiQUpYaFBBbFwvWmdhaEZ1aGFxMGc5Y2hnZ25raG5OOF\
                        wvZzJES0RiWVMyak85Yno5OVlpNXFuajlFQ1VwTGNibUdLTlJqa2xUMUEzanJsempPXC9Wb2xNUGc9PSIsIm1hYyI6IjI3ZjIzNzI3Y2E2Zjg0NGYxODQyZjI1ODMwYTQ\
                            3MGQ0NDFmZmRlNDUwNWQyNTBlNDU2MThhZWJmMzYzZGM3NTUifQ%3D%3D'
    }
    try:
            # 3. 获取网页内容
            print(f"正在访问: {url} ...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # 如果状态码不是200，抛出异常

            # 使用 .prettify() 方法，打印获得的html
            #print(soup.prettify()[:7000] + "\n...")

            # 4. 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            #target_tag1 = soup.find('span', class_='badge rarity-hn')

            target_tag01=soup.select_one('.card-header>.row')
            if target_tag01:
                 target_tag02=target_tag01.contents

                 if len(target_tag02)>2:
                      target_tag1=target_tag02[2]

                      if isinstance(target_tag1,NavigableString):
                           target_tag1=str(target_tag1).strip()
                      else:
                           target_tag1=target_tag1.get_text().strip()
                      
                      print(target_tag1)  

            target_tag2 = soup.find('p', class_='card-text')

            if target_tag1:
                filename=f"{target_tag1}.txt"

            if target_tag2:
                card_text=target_tag2.text

            file_path = os.path.join(save_folder, filename)

            # 6. 下载并保存文本
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(card_text)
                print(f"[成功] {filename}")
            except Exception as e:
                    print(f"[打印失败]")
    except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    target_url = "https://memories.millimas.info/cards/73" 
    
    output_folder = r"C:\Users\Administrator\Desktop\picture\downloaded_images"
    
    download_images_from_url(target_url, 1,2,output_folder)