from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import jieba
import time
import os

# ========== 用户配置 ==========
TXT_PATH = r"C:\Users\Administrator\Desktop\杂\output.txt"     
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"  
CHECK_INTERVAL = 600  
# =============================

# 记录上次文件修改时间
last_modified = None

def generate_wordcloud(text):
    # 示例中文文本
    #text = "Python 是一个非常流行的编程语言，用于数据分析、机器学习和人工智能。"

    # 使用图片作为词云形状
    mask = np.array(Image.open(r"C:\Users\Administrator\Desktop\picture\c13b45f22a0a20f13734685d431db2d3.jpg"))  # 替换图片

    # 中文分词
    text_cut = " ".join(jieba.cut(text))

    # 生成词云
    wc = WordCloud(
        font_path=FONT_PATH,  
        width=800, height=400,
        background_color='black',
        mask=mask,
        contour_color='white',
        contour_width=1
    )

    wc.generate(text_cut)
    wc.to_file(r"C:\Users\Administrator\Desktop\picture\wordcloud.png")  

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def read_chat_file(path):
    """读取聊天记录文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return ""
    
def monitor_chat():
    """定期监控文件变化"""
    global last_modified

    print(f"🔍 正在监控聊天文件: {TXT_PATH}")
    while True:
        if not os.path.exists(TXT_PATH):
            print("⚠️ 文件不存在，等待创建...")
            time.sleep(CHECK_INTERVAL)
            continue

        current_modified = os.path.getmtime(TXT_PATH)
        if last_modified is None or current_modified != last_modified:
            print("📂 检测到聊天记录更新，正在生成词云...")
            text = read_chat_file(TXT_PATH)
            if text.strip():
                generate_wordcloud(text)
            else:
                print("⚠️ 聊天记录为空，跳过。")
            last_modified = current_modified
        else:
            print("⏳ 无变化，等待下一次检查。")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_chat()