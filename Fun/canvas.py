import tkinter as tk
from tkinter import colorchooser

class DrawBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Python 画板")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # 当前颜色和线宽
        self.current_color = "black"
        self.brush_size = 3

        # 画布
        self.canvas = tk.Canvas(root, bg="white", width=580, height=400, relief="sunken", bd=2)
        self.canvas.pack(pady=10)

        #id
        self.shapes=[]
        # 按钮区域
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="🧽 清空", command=self.clear_canvas).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="↩️ 撤销", command=self.undo_last).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="🎨 颜色", command=self.choose_color).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="+", command=self.increase_brush).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="-", command=self.decrease_brush).grid(row=0, column=4, padx=5)

        # 显示线宽
        self.brush_label = tk.Label(button_frame, text=f"线宽: {self.brush_size}")
        self.brush_label.grid(row=0, column=4, padx=5)

        # 鼠标事件绑定
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # 起始点
        self.last_x, self.last_y = None, None
        self.current_stroke=[]

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke=[]

    def end_draw(self,evnet):
        if self.current_stroke:
            self.shapes.append(self.current_stroke)
        self.last_x, self.last_y = None, None

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            line_id=self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color, width=self.brush_size,
                capstyle=tk.ROUND, smooth=True
            )
        self.current_stroke.append(line_id)    
        self.last_x, self.last_y = event.x, event.y

    def undo_last(self):
        if self.shapes:
            last_stroke = self.shapes.pop()  # 取出最后一笔
            for item_id in last_stroke:
                self.canvas.delete(item_id)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear

    def increase_brush(self):
        self.brush_size += 1
        self.brush_label.config(text=f"线宽: {self.brush_size}")

    def decrease_brush(self):
        if self.brush_size > 1:
            self.brush_size -= 1
            self.brush_label.config(text=f"线宽: {self.brush_size}")

# 运行程序
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawBoard(root)
    root.mainloop()
