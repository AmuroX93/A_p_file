import os
from PIL import Image, ImageDraw, ImageFont,ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

def add_subtitles(input_path, output_path, caption_text, bg_color="#FF4F4F", text_color="#FF6868", font_name=None, font_path=None):
    # 以 RGBA 打开原图（确保有 alpha）
    img = Image.open(input_path).convert('RGBA')
    w, h = img.size

    # 透明 overlay，用来绘制半透明背景和文本
    overlay = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(24, w // 12)
    padding = w // 36
    try:
        font = ImageFont.truetype(font_path or "simhei", font_size)
    except Exception:
        font = ImageFont.load_default()

    def draw_subtitles(text):
        if not text:
            return
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        bh = th + padding * 2
        bh_y1 = h
        bh_y0 = h - bh

        # 半透明矩形背景 (RGBA)，这里用黑色 50% 透明，可改为 (r,g,b,alpha)
        rect_rgba = (255, 255, 255, 0)
        draw.rectangle([0, bh_y0, w, bh_y1], fill=rect_rgba)

        text_x = (w - tw) / 2 - bbox[0]
        text_y = bh_y0 + padding

        # 文本颜色：可以传入 hex 字符串或 RGBA tuple (不带 alpha)
        draw.text((text_x, text_y), text, font=font, fill=text_color)

    draw_subtitles(caption_text)

    # 合并 overlay 到原图
    new_img = Image.alpha_composite(img, overlay)

    # 根据输出扩展名决定是否保留 alpha（PNG 保留，JPG 强制转换为 RGB）
    _, ext = os.path.splitext(output_path)
    if ext.lower() == ".png":
        new_img.save(output_path)
    else:
        new_img.convert('RGB').save(output_path)

class titleadder:
    def __init__(self,root):
        self.root=root
        self.root.title("TITLEADDER")
        self.root.geometry("500x500")
        self.root.configure(bg="#BABABA")
        self.root.resizable(False, False)
        self.image_path = None
        self.preview_label = None
        self.custom_font_path=None

        tk.Label(root,text="TITLEADDER",bg="#BABABA",font=("Arial Black", 18, "bold")).pack(pady=10)
        tk.Button(root,text="Select Pictue",bg="#BABABA",font=("Arial Black",18,"bold"),command=self.select_picture).pack(pady=5)
        tk.Label(root,text="TYPE IN",bg="#A9A9A9",font=("Arial Black",12,"bold")).pack(pady=5)
        self.enter_text = tk.Entry(root, bg="#BABABA", font=("simhei", 12), width=40)
        self.enter_text.pack(pady=5)
        tk.Button(root,text="GENERATE",bg="#BABABA",font=("Arial Black", 12),command=self.generate_picture).pack(pady=5)

    def select_picture(self):
        path=filedialog.askopenfilename(title="SELECT PICTURE",filetypes=[("Image Files","*.jpg;*.jpeg;*.png;*.bmp;*.webp")])
        if not path:
            return

        self.image_path = path
        img = Image.open(path)
        img.thumbnail((500, 500))
        self.tk_img = ImageTk.PhotoImage(img)

    def generate_picture(self):
        if not self.image_path:
            messagebox.showerror("ERROR", "SELECT ONE PICTUE!")
            return

        capture_text = self.enter_text.get().strip()
        if not capture_text:
            messagebox.showerror("ERROR", "INPUT TEXT!")
            return

        folder,filename=os.path.split(self.image_path)
        name,ext=os.path.splitext(filename)
        output_path = os.path.join(folder, f"{name}_title{ext}")

        add_subtitles(self.image_path, output_path, caption_text=capture_text)
        messagebox.showinfo("SUCCEEDED", f"SAVED AS:\n{output_path}")

if __name__=="__main__":
    root=tk.Tk()
    app=titleadder(root)
    root.mainloop()

#add_subtitles(r'C:\Users\Administrator\Desktop\picture\c13b45f22a0a20f13734685d431db2d3.jpg',r'C:\Users\Administrator\Desktop\picture\new.jpg', "看看群友在说什么")

