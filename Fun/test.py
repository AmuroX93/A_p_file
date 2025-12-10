import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("通用视频下载器 (基于 yt-dlp)")
        self.root.geometry("600x450")

        # --- 1. URL 输入区域 ---
        input_frame = tk.Frame(root, pady=10)
        input_frame.pack(fill='x', padx=10)
        
        tk.Label(input_frame, text="视频链接:").pack(anchor='w')
        self.url_entry = tk.Entry(input_frame, width=50)
        self.url_entry.pack(fill='x', pady=5)

        # --- 2. 保存路径选择区域 ---
        path_frame = tk.Frame(root, pady=5)
        path_frame.pack(fill='x', padx=10)

        tk.Label(path_frame, text="保存目录:").pack(anchor='w')
        
        path_select_frame = tk.Frame(path_frame)
        path_select_frame.pack(fill='x', pady=5)
        
        self.path_entry = tk.Entry(path_select_frame)
        self.path_entry.pack(side='left', fill='x', expand=True)
        # 默认保存路径为当前目录下的 Downloads
        default_path = os.path.join(os.getcwd(), "Downloads")
        self.path_entry.insert(0, default_path)

        tk.Button(path_select_frame, text="浏览...", command=self.browse_folder).pack(side='right', padx=5)

        # --- 3. 下载按钮 ---
        btn_frame = tk.Frame(root, pady=10)
        btn_frame.pack()
        
        self.download_btn = tk.Button(btn_frame, text="开始下载", command=self.start_download_thread, 
                                      bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20)
        self.download_btn.pack()

        # --- 4. 日志输出区域 ---
        log_frame = tk.Frame(root, pady=10)
        log_frame.pack(fill='both', expand=True, padx=10)
        
        tk.Label(log_frame, text="下载日志:").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled', bg="#f0f0f0")
        self.log_text.pack(fill='both', expand=True)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def log(self, message):
        """向日志窗口添加信息"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # 自动滚动到底部
        self.log_text.config(state='disabled')

    def start_download_thread(self):
        """在单独的线程中启动下载，避免界面卡死"""
        url = self.url_entry.get().strip()
        folder = self.path_entry.get().strip()

        if not url:
            messagebox.showwarning("提示", "请输入视频链接！")
            return
        
        if not folder:
            messagebox.showwarning("提示", "请选择保存目录！")
            return

        # 禁用按钮防止重复点击
        self.download_btn.config(state='disabled', text="下载中...")
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END) # 清空日志
        self.log_text.config(state='disabled')
        
        # 启动线程
        thread = threading.Thread(target=self.run_ytdlp, args=(url, folder))
        thread.daemon = True
        thread.start()

    def run_ytdlp(self, url, folder):
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
                self.log(f"📂 创建目录: {folder}")

            output_template = os.path.join(folder, '%(title)s.%(ext)s')
            
            # 隐藏命令行窗口 (仅限 Windows)
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            command = [
                'yt-dlp',
                '--newline', # 关键：让进度条换行显示，方便捕获
                '--ignore-errors',
                '-f', 'bestvideo+bestaudio/best',
                '--merge-output-format', 'mp4',
                '-o', output_template,
                url
            ]

            self.log(f"🚀 开始下载: {url}")
            self.log("-" * 30)

            # 使用 Popen 实时获取输出
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # 逐行读取输出
            for line in process.stdout:
                line = line.strip()
                if line:
                    # 在主线程更新 GUI 需要注意，但简单的 insert 通常兼容性尚可
                    # 或者使用 root.after 包装
                    self.log(line)

            process.wait()

            if process.returncode == 0:
                self.log("\n✅ 下载完成！")
                messagebox.showinfo("成功", "视频下载完成！")
            else:
                self.log(f"\n❌ 下载出错，返回码: {process.returncode}")
                messagebox.showerror("错误", "下载过程中发生错误，请查看日志。")

        except FileNotFoundError:
            self.log("❌ 错误: 未找到 yt-dlp 程序。")
            self.log("请确保 yt-dlp.exe 在同一目录下或已配置环境变量。")
            messagebox.showerror("缺少组件", "找不到 yt-dlp.exe")
        except Exception as e:
            self.log(f"❌ 未知错误: {e}")
            messagebox.showerror("错误", str(e))
        finally:
            # 恢复按钮状态
            self.root.after(0, lambda: self.download_btn.config(state='normal', text="开始下载"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()