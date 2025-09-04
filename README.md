# 视频转音频工具（Video to Audio Converter）

一个基于Python + Tkinter + FFmpeg开发的轻量视频转音频工具，支持多格式输入输出、音质调节，界面简洁易用，无需复杂操作即可快速提取视频中的音频。


## 📋 项目介绍
- **技术栈**：Python 3.x、Tkinter（GUI界面）、FFmpeg（音视频处理核心）
- **核心功能**：从视频中提取音频，支持自定义输出格式和音质
- **适用场景**：日常提取视频BGM、会议录音、网课音频等
- **跨平台**：支持Windows/Mac/Linux（需配置FFmpeg）


## ✨ 功能特性
1. **多格式支持**：
   - 输入：MP4、MOV、AVI、FLV、MKV、WMV、MPG等常见视频格式
   - 输出：MP3、WAV、FLAC、AAC等主流音频格式
2. **音质可调**：提供64k、128k、192k、256k、320k比特率选择，适配不同需求（高音质收藏/低音质省空间）
3. **直观交互**：
   - 图形化界面（GUI），支持拖拽/点击选择文件
   - 实时转换进度条显示，支持中途取消操作
   - 转换完成自动提示保存路径
4. **轻量无依赖**：仅依赖Python标准库 + FFmpeg，无需额外安装第三方Python包


## 🚀 环境准备
使用前需完成以下2步准备（本地运行/打包exe均需）：

### 1. 安装Python
- 版本要求：Python 3.6+
- 下载地址：[Python官网](https://www.python.org/downloads/)
- 验证：安装后打开命令行，输入 `python --version` 或 `python3 --version`，显示版本号即成功

### 2. 安装FFmpeg（核心依赖）
FFmpeg是处理音视频的底层工具，必须安装并配置到系统环境变量中：

| 系统   | 安装方法                                                                 | 验证命令          |
|--------|--------------------------------------------------------------------------|-------------------|
| Windows| 1. 从[FFmpeg官网](https://ffmpeg.org/download.html#build-windows)下载「Full Build」<br>2. 解压后将 `bin` 目录（含ffmpeg.exe）添加到系统环境变量<br>3. 重启命令行 | `ffmpeg -version` |
| Mac    | 1. 先安装Homebrew（若未安装）：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`<br>2. 安装FFmpeg：`brew install ffmpeg` | `ffmpeg -version` |
| Linux  | 直接执行：`sudo apt update && sudo apt install ffmpeg`                   | `ffmpeg -version` |

> 注意：若验证命令提示“找不到ffmpeg”，需重新检查环境变量配置或重启设备。


## 📖 使用方法
### 方法1：直接运行Python脚本（适合开发者）
1. 克隆本仓库到本地：
   ```bash
   git clone https://github.com/你的GitHub用户名/视频转音频工具仓库名.git
   cd 视频转音频工具仓库名
