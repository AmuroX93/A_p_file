import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class MemeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ P图表情包制作器")
        self.root.geometry("800x700")
        self.root.configure(bg="#f5f5f5")

        self.image_path = None
        self.base_img = None
        self.tk_img = None
        self.canvas_img = None
        self.text_items = []  # 存放添加的文字对象

        # --- 顶部按钮区 ---
        toolbar = tk.Frame(root, bg="#e0e0e0")
        toolbar.pack(fill="x", pady=5)

        tk.Button(toolbar, text="📂 打开图片", command=self.open_image).pack(side="left", padx=5)
        tk.Button(toolbar, text="📝 添加文字", command=self.add_text).pack(side="left", padx=5)
        tk.Button(toolbar, text="💾 保存图片", command=self.save_image).pack(side="left", padx=5)

        # --- 画布区 ---
        self.canvas = tk.Canvas(root, width=750, height=600, bg="#ccc")
        self.canvas.pack(pady=10)

        # 拖动文字用
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图像文件", "*.jpg;*.jpeg;*.png;*.bmp;*.webp")]
        )
        if not path:
            return

        self.image_path = path
        self.base_img = Image.open(path)
        self.show_image(self.base_img)

    def show_image(self, pil_img):
        img = pil_img.copy()
        img.thumbnail((750, 600))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas_img = self.canvas.create_image(375, 300, image=self.tk_img)

    def add_text(self):
        if not self.base_img:
            messagebox.showerror("错误", "请先打开一张图片")
            return

        text = simple_input("请输入文字内容：")
        if not text:
            return

        item = self.canvas.create_text(
            375, 550,
            text=text,
            fill="white",
            font=("Impact", 32, "bold"),
            anchor="center",
            outline="black"
        )
        self.text_items.append(item)

    # --- 拖拽事件 ---
    def on_drag_start(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item and item[0] in self.text_items:
            self.drag_data["item"] = item[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag_release(self, event):
        self.drag_data["item"] = None

    def save_image(self):
        if not self.base_img:
            messagebox.showerror("错误", "没有图片可保存！")
            return

        save_path = filedialog.asksaveasfilename(
            title="保存表情包",
            defaultextension=".png",
            filetypes=[("PNG 文件", "*.png"), ("JPEG 文件", "*.jpg")]
        )
        if not save_path:
            return

        # 生成带文字的新图
        output = self.base_img.copy()
        draw = ImageDraw.Draw(output)
        for item in self.text_items:
            x, y = self.canvas.coords(item)
            text = self.canvas.itemcget(item, "text")
            font = ImageFont.truetype("Impact.ttf", 50)
            # 文字描边
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    draw.text((x + dx, y + dy), text, font=font, fill="black")
            draw.text((x, y), text, font=font, fill="white")

        output.save(save_path)
        messagebox.showinfo("成功", f"表情包已保存：\n{save_path}")

# --- 简易文字输入对话框 ---
def simple_input(prompt):
    top = tk.Toplevel()
    top.title("输入文字")
    top.geometry("300x120")
    tk.Label(top, text=prompt).pack(pady=10)
    entry = tk.Entry(top)
    entry.pack(pady=5)
    result = []

    def ok():
        result.append(entry.get())
        top.destroy()
    tk.Button(top, text="确定", command=ok).pack()
    top.wait_window()
    return result[0] if result else None

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeEditor(root)
    root.mainloop()
