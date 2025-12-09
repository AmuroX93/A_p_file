import os
from PIL import Image, ImageDraw, ImageFont,ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

def make_meme(input_path, output_path, bottom_text='',bg_color=(255, 255, 255),font_name=None,font_path=None):
    img = Image.open(input_path).convert('RGB')
    #draw = ImageDraw.Draw(img)
    w, h = img.size
    add_h=int(h*0.2)
    new_h=h+add_h

    new_img = Image.new('RGB', (w, new_h), bg_color)
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)

    font_size = max(24, w // 12)
    try:
        # 优先使用自定义字体文件
        if font_path and os.path.isfile(font_path):
            font=ImageFont.truetype(font_path,font_size)
        else:
            try:
                font = ImageFont.truetype("msyh", font_size)
            except:
                font = ImageFont.truetype("simhei", font_size)
    except Exception:
        font=ImageFont.load_default()

    #arial英文

    def draw_text(text, y):
        if not text: return
        text = text.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x = (w - tw) / 2
        # 描边
        stroke = max(2, font_size // 15)
        for dx in range(-stroke, stroke+1):
            for dy in range(-stroke, stroke+1):
                #draw.text((x+dx, 9*th+dy), text, font=font, fill='black')
                draw.text((x+dx, y+(3/4*th)+dy), text, font=font, fill='black')
        #draw.text((x, 9*th), text, font=font, fill='white')
        draw.text((x, y+(3/4*th)), text, font=font, fill='white')

    draw_text(bottom_text, h)
    new_img.save(output_path)
    return new_img

# --- GUI部分 ---
class MemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MEMEMAKER")
        self.root.geometry("500x500")
        self.root.configure(bg="#3c3b50")
        self.root.resizable(False, False)

        self.image_path = None
        self.preview_label = None
        self.custom_font_path=None

        # 标题
        tk.Label(root, text="MEME_MAKER", bg="#A9A9A9",font=("Arial Black", 18, "bold")).pack(pady=10)

        # 图片选择按钮
        tk.Button(root, text="📁 SELECT_PICTURE",bg="#A9A9A9", font=("Arial Black", 12), command=self.select_image).pack(pady=5)

        # 图片预览区
        self.preview = tk.Label(root, text="NONE PICTURE", width=50, height=10, bg="#797979", relief="ridge")
        self.preview.pack(pady=8)

        # 输入框
        tk.Label(root, text="TYPEIN:", bg="#A9A9A9",font=("Arial Black", 12)).pack(pady=5)
        self.text_entry = tk.Entry(root,bg="#D4D4D4", font=("Arial Black", 12), width=40)
        self.text_entry.pack(pady=5)

        #下拉框
        tk.Label(root,text="FONT:",bg="#A9A9A9",font=("Arial Black",12)).pack(pady=5)
        self.font_var = tk.StringVar(value="msyh")
        font_options = ["msyh", "simhei", "arial", "impact", "系统默认"]
        tk.OptionMenu(root, self.font_var, *font_options).pack(pady=2)
        tk.Button(root, text="📂 LOAD FONT FILE", bg="#A9A9A9", font=("Arial Black", 10), command=self.load_font_file).pack(pady=2)
        self.custom_font_label = tk.Label(root, text="", bg="#3c3b50", fg="lightgray", font=("Arial Black", 9))
        self.custom_font_label.pack(pady=(0,5))

        # 生成按钮
        tk.Button(root, text="🎨 GENERATED", font=("Arial Black", 13, "bold"), bg="#346E36", fg="white", command=self.generate_meme).pack(pady=15)

        # 状态提示
        self.status = tk.Label(root, text="", font=("Arial Black", 10), fg="gray")
        self.status.pack(pady=5)

    def load_font_file(self):
        path = filedialog.askopenfilename(
            title="SELECT FONT FILE",
            filetypes=[("Font Files", "*.ttf;*.otf")]
        )
        if not path:
            return
        self.custom_font_path = path
        self.custom_font_label.config(text=f"自定义字体: {os.path.basename(path)}")
        self.status.config(text=f"LOADED FONT:{os.path.basename(path)}")

    def select_image(self):
        path = filedialog.askopenfilename(
            title="SELECT PICTUE",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.webp")]
        )
        if not path:
            return

        self.image_path = path
        img = Image.open(path)
        img.thumbnail((500, 500))
        self.tk_img = ImageTk.PhotoImage(img)
        self.preview.config(image=self.tk_img, text="")
        self.status.config(text=f"SELECTED:{os.path.basename(path)}")

    def generate_meme(self):
        if not self.image_path:
            messagebox.showerror("ERROR", "SELECT ONE PICTUE!")
            return

        bottom_text = self.text_entry.get().strip()
        if not bottom_text:
            messagebox.showerror("ERROR", "INPUT TEXT!")
            return

        folder, filename = os.path.split(self.image_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(folder, f"{name}_meme{ext}")

        try:
            font_name = self.font_var.get()
            font_path = getattr(self, 'custom_font_path', None)
            new_img = make_meme(self.image_path, output_path, bottom_text=bottom_text,
                                font_name=(None if font_name == "系统默认" else font_name),
                                font_path=font_path)
            messagebox.showinfo("SUCCEEDED", f"SAVED AS:\n{output_path}")

            # 更新预览为生成后的图（不修改用于保存的 new_img，先复制一份）
            preview_img = new_img.copy()
            preview_img.thumbnail((500, 500))
            self.tk_img = ImageTk.PhotoImage(preview_img)
            self.preview.config(image=self.tk_img, text="")
            self.status.config(text=f"GENERATED {os.path.basename(output_path)}")

        except Exception as e:
            messagebox.showerror("ERROR", str(e))

# --- 主程序入口 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeApp(root)
    root.mainloop()

#make_meme(r"C:\Users\Administrator\Desktop\picture\polangwanzhang.jpg",\
#           r"C:\Users\Administrator\Desktop\p_file\mememaker\meme_out.jpg",\
#              bottom_text="This is producer")
#图片外起名！
#半命题！
#自动输出命名！
#字体颜色选择
