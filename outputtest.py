import os
from openpyxl import Workbook
from openpyxl.styles import Alignment
import trafilatura


# ----------- 文本切割函数 -----------
def split_text_by_length(text, max_len=20):
    """将文本按指定最大长度切割，优先在‘／’或‘/’处分行"""
    parts = []
    current_line = ""
    segments = text.replace("/", "／").split("／")

    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        if len(current_line) + len(seg) + 1 <= max_len:
            current_line += ("／" if current_line else "") + seg
        else:
            parts.append(current_line)
            current_line = seg
    if current_line:
        parts.append(current_line)

    return parts


# ----------- 网页抓取函数 -----------
def fetch_web_text(url):
    """从网页提取正文文本"""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print("无法抓取网页，请检查网址是否正确。")
        return ""
    text = trafilatura.extract(downloaded)
    return text or ""


# ----------- Excel 保存函数 -----------
def save_to_excel(text, output_folder=r"C:\Users\Administrator\Desktop\杂\Webdata", filename="from_web.xlsx", max_len=20):
    """将提取的网页文本切割并写入 Excel"""
    os.makedirs(output_folder, exist_ok=True)
    excel_path = os.path.join(output_folder, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "网页内容"

    # 按行处理文本并写入
    for i, line in enumerate(text.strip().split("\n"), start=1):
        wrapped_lines = split_text_by_length(line, max_len=max_len)
        ws.cell(row=i, column=1, value="\n".join(wrapped_lines))

    # 设置自动换行
    for column in ws.columns:
        for cell in column:
            cell.alignment = Alignment(wrap_text=True)

    wb.save(excel_path)
    print(f"已保存到：{excel_path}")


# ----------- 主流程 -----------
if __name__ == "__main__":
    url="https://bgm.tv/ep/160178"
    #url = input("请输入要抓取的网页链接：").strip()
    text = fetch_web_text(url)

    if text:
        save_to_excel(text, max_len=40)
    else:
        print("没有提取到有效文本。")

#提取多一行
#新增提取