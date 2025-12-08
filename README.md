# 简易视频分享 / Simple Video Share

一个简单的局域网视频分享页面，适用于没有互联网但有局域网的环境（例如工地）。

A simple LAN video sharing web page, suitable for environments without internet but with local network access (e.g., construction sites).

## 功能特性 / Features

- 📤 **视频上传** - 支持拖拽或选择文件上传
- 📚 **视频列表** - 自动显示所有已上传的视频
- ▶️ **在线播放** - 直接在浏览器中播放视频
- 🌐 **局域网访问** - 同一局域网内的所有设备都可以访问
- 🎨 **简洁界面** - 清晰直观的用户界面
- 📱 **响应式设计** - 支持手机、平板和电脑访问

- 📤 **Video Upload** - Support drag-and-drop or file selection
- 📚 **Video Library** - Automatically display all uploaded videos
- ▶️ **Online Playback** - Play videos directly in the browser
- 🌐 **LAN Access** - Accessible from all devices on the same local network
- 🎨 **Clean Interface** - Clear and intuitive user interface
- 📱 **Responsive Design** - Support for mobile, tablet, and desktop

## 系统要求 / Requirements

- Python 3.x (服务器端 / server-side)
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

## 快速开始 / Quick Start

### 1. 启动服务器 / Start the Server

```bash
# 进入项目目录 / Navigate to project directory
cd simple_video_share

# 运行服务器 / Run the server
python3 server.py
```

服务器将在 8000 端口启动。你将看到如下输出：

The server will start on port 8000. You will see output like:

```
🎬 Simple Video Share Server
📡 Server running at http://localhost:8000/
📂 Videos stored in: /path/to/simple_video_share/videos/
🌐 Access from other devices using your local IP address
⏹  Press Ctrl+C to stop the server
```

### 2. 访问应用 / Access the Application

**在本机访问 / On the same computer:**
- 打开浏览器访问 / Open browser and visit: `http://localhost:8000`

**从其他设备访问 / From other devices:**

1. 首先找到运行服务器的电脑的局域网 IP 地址：

   First, find the LAN IP address of the computer running the server:

   **Windows:**
   ```bash
   ipconfig
   # 查找 "IPv4 地址" / Look for "IPv4 Address"
   ```

   **Mac/Linux:**
   ```bash
   ifconfig
   # 或 / or
   ip addr show
   # 查找形如 192.168.x.x 的地址 / Look for address like 192.168.x.x
   ```

2. 然后在同一局域网的其他设备上访问：

   Then access from other devices on the same network:
   ```
   http://[服务器IP地址]:8000
   # 例如 / For example: http://192.168.1.100:8000
   ```

### 3. 使用应用 / Using the Application

1. **上传视频 / Upload Videos**
   - 点击上传区域选择视频文件 / Click the upload area to select video files
   - 或者直接拖拽视频到上传区域 / Or drag and drop videos to the upload area
   - 支持格式：MP4, WebM, OGG, MOV, AVI

2. **播放视频 / Play Videos**
   - 在视频列表中点击任意视频 / Click any video in the video list
   - 视频将在播放器中自动播放 / Video will automatically play in the player

3. **刷新列表 / Refresh List**
   - 点击"刷新列表"按钮查看最新上传的视频 / Click "Refresh List" button to see newly uploaded videos

## 技术栈 / Technology Stack

- **后端 / Backend**: Python 3 (标准库 / standard library)
- **前端 / Frontend**: HTML5, CSS3, JavaScript (原生 / vanilla)
- **视频播放 / Video Player**: HTML5 Video API

## 文件结构 / File Structure

```
simple_video_share/
├── server.py          # Python 服务器 / Python server
├── index.html         # 主页面 / Main page
├── style.css          # 样式文件 / Stylesheet
├── script.js          # JavaScript 脚本 / JavaScript
├── videos/            # 视频存储目录 (自动创建) / Video storage (auto-created)
├── .gitignore         # Git 忽略文件 / Git ignore file
└── README.md          # 说明文档 / Documentation
```

## 注意事项 / Notes

- 📁 视频文件会保存在 `videos/` 目录中
- 🔒 请确保局域网环境安全，因为所有设备都可以访问和上传视频
- 💾 根据需要定期清理旧视频以节省存储空间
- 🌐 如果需要修改端口，可以编辑 `server.py` 中的 `PORT` 变量

- 📁 Video files are stored in the `videos/` directory
- 🔒 Ensure your LAN environment is secure as all devices can access and upload videos
- 💾 Periodically clean old videos to save storage space as needed
- 🌐 To change the port, edit the `PORT` variable in `server.py`

## 故障排除 / Troubleshooting

**无法访问服务器 / Cannot access server:**
- 检查防火墙设置是否阻止了 8000 端口 / Check if firewall is blocking port 8000
- 确认服务器和客户端在同一局域网内 / Verify server and client are on the same LAN

**视频无法播放 / Video cannot play:**
- 确认浏览器支持该视频格式 / Confirm browser supports the video format
- 尝试转换视频为 MP4 格式 / Try converting video to MP4 format

**上传失败 / Upload fails:**
- 检查服务器磁盘空间 / Check server disk space
- 确认有写入 `videos/` 目录的权限 / Verify write permissions for `videos/` directory

## 许可证 / License

MIT License

---

💡 **提示 / Tip**: 这个项目专为局域网环境设计，无需互联网连接即可使用！

💡 **Tip**: This project is designed for LAN environments and works without internet connection!