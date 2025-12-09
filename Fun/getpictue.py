import os
import requests
from bs4 import BeautifulSoup
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

    # 2. 循环遍历每一页
    for page_num in range(start_page, end_page + 1):
        print(f"\n====== 正在处理第 {page_num} 页 ======")
        
        # 构造当页的 URL (根据实际网站结构调整)
        # 假设网站是 ?page=1 这种格式
        url = f"{url}?page={page_num}" 
        

        try:
            # 3. 获取网页内容
            print(f"正在访问: {url} ...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # 如果状态码不是200，抛出异常

            # 使用 .prettify() 方法，打印获得的html
            #print(soup.prettify()[:7000] + "\n...")

            # 4. 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            print(f"找到 {len(img_tags)} 个图片标签，准备开始下载...")
            count = 0
            for img in img_tags:
                # 获取图片src
                img_url = img.get('src')
            
                if not img_url:
                    continue

                img_url = urljoin(url, img_url)

                # 过滤掉非 http 开头的无效链接 (如 base64 数据)
                if not img_url.startswith('http'):
                    continue

                # 5. 生成文件名
                # 解析 URL 获取路径部分
                parsed_path = urlparse(img_url).path
                # 获取文件名
                filename = os.path.basename(parsed_path)
            
                # 如果文件名为空或太长，给一个默认名字
                if not filename or len(filename) > 50:
                    filename = f"image_{page_num}_{count}.jpg"
            
                # 拼接完整保存路径
                file_path = os.path.join(save_folder, filename)

                # 6. 下载并保存图片
                try:
                    img_data = requests.get(img_url, headers=headers, timeout=10).content
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    print(f"[成功] {filename}")
                    count += 1
                except Exception as e:
                    print(f"[失败] 无法下载 {img_url}: {e}")

            count2+=count

            print(f"\n下载完成！共成功下载 {count2} 张图片。")

        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    target_url = "https://memories.millimas.info/cards" 
    
    output_folder = r"C:\Users\Administrator\Desktop\picture\downloaded_images"
    
    download_images_from_url(target_url, 1,2,output_folder)