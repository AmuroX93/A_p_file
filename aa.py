import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# --- 核心代码模板 ---
def get_rendered_html_with_selenium(target_url, wait_time=5):
    """
    使用 Selenium 启动浏览器，等待页面完全加载（包括 JavaScript），并返回最终的 HTML。
    """
    
    # 1. 设置 Service，自动安装和管理 ChromeDriver
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    except Exception as e:
        print(f"❌ 启动浏览器失败，请检查 Chrome 浏览器是否已安装或驱动管理器是否正确安装: {e}")
        return None

    print(f"浏览器已启动，正在访问: {target_url} ...")
    driver.get(target_url)
    
    # 2. 核心步骤：等待 JavaScript 执行
    # driver.implicitly_wait(10) 会等待元素出现，但有时不够
    # 强制等待 (sleep) 是一种更可靠的确保内容加载完成的方法
    print(f"等待 {wait_time} 秒，确保 JavaScript 内容完全加载...")
    time.sleep(wait_time) 
    
    # 3. 获取浏览器中渲染完成的最终 HTML 源代码
    full_html = driver.page_source
    
    # 4. 关闭浏览器
    driver.quit()
    print("浏览器已关闭，获取到完整的 HTML 源代码。")
    
    return full_html

# --- 主程序部分 ---
if __name__ == "__main__":
    # 请替换为您需要爬取的网址
    TARGET_URL = "https://memories.millimas.info/cards" 
    OUTPUT_FOLDER = "selenium_downloads"
    
    # 获取渲染后的完整 HTML
    html_content = get_rendered_html_with_selenium(TARGET_URL)
    
    if html_content:
        # 5. 使用 BeautifulSoup 解析完整的 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 6. 搜索您缺失的子元素信息 (例如搜索所有的图片标签)
        # 现在，之前缺失的子元素应该可以被找到
        img_tags = soup.find_all('img')
        
        print("-" * 30)
        print(f"使用 BeautifulSoup 成功找到图片标签数量: {len(img_tags)}")
        
        if img_tags:
            print(f"第一个图片的 SRC 属性: {img_tags[0].get('src')}")
            # 现在，您可以结合之前讨论的下载逻辑，对这些找到的图片进行批量下载。
        else:
            print("警告: 即使使用 Selenium，也未能找到图片标签。请检查 TARGET_URL 是否正确。")

# --- 额外说明 ---
# 运行此脚本时，请使用您指定的 Python 3.13 解释器：
# "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" your_script_name.py