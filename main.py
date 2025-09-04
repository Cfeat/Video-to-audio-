import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess
import threading
import time

class VideoToAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("视频转音频工具")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TCombobox", font=("SimHei", 10))
        
        # 视频文件路径
        self.video_path = tk.StringVar()
        # 输出格式
        self.output_format = tk.StringVar(value="mp3")
        # 输出质量
        self.quality = tk.StringVar(value="192k")
        
        # 创建界面
        self.create_widgets()
        
        # 转换线程标志
        self.converting = False

    def create_widgets(self):
        # 标题
        title_label = ttk.Label(self.root, text="视频转音频工具", font=("SimHei", 16, "bold"))
        title_label.pack(pady=15)
        
        # 文件选择区域
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill=tk.X, padx=50, pady=10)
        
        ttk.Label(file_frame, text="视频文件:").pack(side=tk.LEFT, padx=5)
        
        file_entry = ttk.Entry(file_frame, textvariable=self.video_path, width=40)
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(file_frame, text="浏览", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 设置区域
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(fill=tk.X, padx=50, pady=10)
        
        ttk.Label(settings_frame, text="输出格式:").pack(side=tk.LEFT, padx=5)
        
        format_combo = ttk.Combobox(settings_frame, textvariable=self.output_format, 
                                   values=["mp3", "wav", "flac", "aac"], width=10)
        format_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(settings_frame, text="音质:").pack(side=tk.LEFT, padx=5)
        
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality, 
                                    values=["64k", "128k", "192k", "256k", "320k"], width=10)
        quality_combo.pack(side=tk.LEFT, padx=5)
        
        # 进度区域
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=50, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        self.status_label = ttk.Label(self.root, text="就绪", foreground="blue")
        self.status_label.pack(pady=10)
        
        # 按钮区域
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        self.convert_btn = ttk.Button(btn_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=10)
        
        self.cancel_btn = ttk.Button(btn_frame, text="取消", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # 底部信息
        info_label = ttk.Label(self.root, text="支持格式: MP4, MOV, AVI, FLV, MKV 等", font=("SimHei", 9), foreground="gray")
        info_label.pack(side=tk.BOTTOM, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.mov *.avi *.flv *.mkv *.wmv *.mpg *.mpeg")]
        )
        if file_path:
            self.video_path.set(file_path)

    def start_conversion(self):
        video_path = self.video_path.get()
        
        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("错误", "请选择有效的视频文件")
            return
        
        self.converting = True
        self.convert_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.status_label.config(text="转换中...", foreground="orange")
        self.progress_var.set(0)
        
        # 在新线程中执行转换，避免界面冻结
        threading.Thread(target=self.convert_video, args=(video_path,), daemon=True).start()
        # 进度更新线程
        threading.Thread(target=self.update_progress, daemon=True).start()

    def cancel_conversion(self):
        self.converting = False
        self.status_label.config(text="已取消", foreground="red")
        self.convert_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)

    def convert_video(self, video_path):
        try:
            # 获取输出文件名
            output_format = self.output_format.get()
            quality = self.quality.get()
            file_name = os.path.splitext(video_path)[0]
            output_path = f"{file_name}.{output_format}"
            
            # 使用ffmpeg进行转换
            # 命令说明: -i 输入文件 -vn 禁用视频 -ab 音频比特率 -y 覆盖输出文件
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vn",  # 不包含视频
                "-ab", quality,  # 音频比特率
                "-y",  # 覆盖输出文件
                output_path
            ]
            
            # 执行命令
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if self.converting:
                self.root.after(0, lambda: self.status_label.config(text="转换完成!", foreground="green"))
                self.root.after(0, lambda: messagebox.showinfo("成功", f"音频已保存至:\n{output_path}"))
        except Exception as e:
            if self.converting:
                self.root.after(0, lambda: self.status_label.config(text="转换失败", foreground="red"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"转换失败: {str(e)}"))
        finally:
            if self.converting:
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.cancel_btn.config(state=tk.DISABLED))
            self.converting = False

    def update_progress(self):
        # 简单的进度模拟，实际项目中可以解析ffmpeg的输出获取真实进度
        while self.converting and self.progress_var.get() < 100:
            current = self.progress_var.get()
            if current < 95:  # 留一些空间给最后完成
                self.root.after(0, lambda: self.progress_var.set(current + 0.5))
            time.sleep(0.1)

if __name__ == "__main__":
    # 检查ffmpeg是否安装
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到ffmpeg，请先安装ffmpeg并确保它在系统PATH中")
        exit(1)
        
    root = tk.Tk()
    app = VideoToAudioConverter(root)
    root.mainloop()
