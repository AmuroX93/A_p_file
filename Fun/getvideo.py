import subprocess
import os
import sys

def download_video(video_url, output_folder):
    
    # 创建存储文件夹
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"📂 已创建保存目录: {output_folder}")
        except OSError as e:
            print(f"❌ 创建目录失败: {e}")
            return

    # 2. 构建 yt-dlp 命令
    # -o 选项指定输出模板：路径/文件名.扩展名
    # %(title)s 会被替换为视频标题，%(ext)s 会被替换为扩展名
    output_template = os.path.join(output_folder, '%(title)s.%(ext)s')
    
    command = [
        'yt-dlp',                       # 命令名称
        '--newline',                    # 在新行输出进度，方便 Python 捕获
        '--ignore-errors',              # 遇到错误继续（如下载列表时）
        '-f', 'bestvideo+bestaudio/best', # 下载最佳画质+最佳音质，或者最佳单一文件
        '--merge-output-format', 'mp4', # 如果需要合并，合并为 mp4 (需要安装 FFmpeg)
        '-o', output_template,          # 指定输出路径和文件名格式
        video_url                       # 视频链接
    ]

    print(f"🚀 正在准备下载: {video_url}")
    print(f"💾 保存位置: {output_folder}")
    print("-" * 50)

    try:
        # 3. 调用命令行执行下载
        # check=True 表示如果命令返回错误代码（非0），则抛出异常
        subprocess.run(command, check=True)
        print("\n✅ 下载任务完成！")

    except FileNotFoundError:
        print("\n❌ 错误: 系统找不到 'yt-dlp' 命令。")
        print("请确保您已安装它: pip install yt-dlp")
        print("并确保将其添加到了系统环境变量中。")
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 下载过程中出错 (错误码 {e.returncode})。")
        print("常见原因: 网络问题、URL 无效或该视频需要登录/Cookie。")
        
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")

# --- 主程序入口 ---
if __name__ == "__main__":
    # 在这里输入您的视频链接
    target_url = r"https://www.nicovideo.jp/watch/sm20504554"  # 示例链接
    
    # 在这里输入您想保存的路径 (支持相对路径或绝对路径)
    # 例如: "D:\\Downloads\\Videos" 或 "./my_videos"
    save_dir = r"D:\video\source"

    download_video(target_url, save_dir)