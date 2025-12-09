from flask import Flask, send_file, request, jsonify, render_template_string, session
import os
import secrets
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate random secret key for session

VIDEO_ROOT = r'D:\videos-share-resouce'
SECRET_VIDEO_ROOT = r'D:\videos-secret-resouce'
SECRET_PASSWORD = 'secret'

# Store valid tokens and expiration times
valid_tokens = {}

# Get video list
def get_video_list(is_secret=False):
    video_root = SECRET_VIDEO_ROOT if is_secret else VIDEO_ROOT
    video_files = []
    
    # Return empty list if directory doesn't exist
    if not os.path.exists(video_root):
        return video_files
    
    for root, dirs, files in os.walk(video_root):
        for file in files:
            if file.lower().endswith(('.mp4', '.webm', '.ogg', '.mkv', '.rmvb', '.avi', '.flv', '.mov')):
                rel_dir = os.path.relpath(root, video_root)
                rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                video_files.append(rel_file.replace('\\', '/'))
    return video_files

# Clean expired tokens
def clean_expired_tokens():
    current_time = time.time()
    # Only delete truly expired tokens (positive timestamp and expired), don't delete used tokens (-1)
    expired = [token for token, exp_time in valid_tokens.items() if exp_time > 0 and current_time > exp_time]
    for token in expired:
        del valid_tokens[token]

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(x in user_agent for x in ['mobile', 'android', 'iphone', 'ipad', 'ipod'])
    
    # Check if there's a secret space token
    secret_token = request.args.get('secretnumber', '')
    is_secret_mode = False
    
    if secret_token:
        clean_expired_tokens()
        if secret_token in valid_tokens:
            token_status = valid_tokens[secret_token]
            # Only unused tokens (positive timestamp) can access
            if token_status > 0:
                # Token is valid and newly generated, allow access to secret mode
                is_secret_mode = True
                # Mark token as used (set to -1 to indicate used, cannot be used to access homepage again)
                valid_tokens[secret_token] = -1
            else:
                # Token already used (-1), don't allow access again
                return render_template_string('<script>alert("Access link has expired and cannot be reused!"); window.location.href="/";</script>')
        else:
            # Token invalid or expired, redirect to normal mode
            return render_template_string('<script>alert("Access link has expired!"); window.location.href="/";</script>')
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Video Sharing Center</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            display: flex;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow: hidden;
        }
        
        body.mobile {
            flex-direction: column;
        }
        
        #sidebar {
            width: 320px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 2px 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: all 0.3s ease;
            z-index: 100;
            display: flex;
            flex-direction: column;
        }
        
        /* Mobile sidebar styles */
        body.mobile #sidebar {
            width: 100%;
            height: 40vh;
            position: fixed;
            bottom: 0;
            left: 0;
            border-radius: 20px 20px 0 0;
            box-shadow: 0 -5px 30px rgba(0,0,0,0.3);
            transform: translateY(0);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        body.mobile #sidebar.collapsed {
            transform: translateY(calc(100% - 60px));
        }
        
        #sidebar::-webkit-scrollbar { width: 8px; }
        #sidebar::-webkit-scrollbar-track { background: #f1f1f1; }
        #sidebar::-webkit-scrollbar-thumb { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        #sidebar::-webkit-scrollbar-thumb:hover { background: #764ba2; }
        
        .scrollable-content::-webkit-scrollbar { width: 6px; }
        .scrollable-content::-webkit-scrollbar-track { background: #f1f1f1; }
        .scrollable-content::-webkit-scrollbar-thumb { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
        .scrollable-content::-webkit-scrollbar-thumb:hover { background: #764ba2; }
        
        .sidebar-header {
            padding: 25px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            position: relative;
            cursor: pointer;
            user-select: none;
            flex-shrink: 0;
        }
        
        body.mobile .sidebar-header {
            padding: 15px 20px;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }
        
        .toggle-icon {
            display: none;
            font-size: 20px;
            transition: transform 0.3s;
        }
        
        body.mobile .toggle-icon {
            display: block;
        }
        
        body.mobile #sidebar.collapsed .toggle-icon {
            transform: rotate(180deg);
        }
        
        .search-box {
            padding: 15px;
            background: white;
            border-bottom: 1px solid #e0e0e0;
            flex-shrink: 0;
        }
        
        body.mobile .search-box {
            flex-shrink: 0;
        }
        
        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s;
        }
        
        .search-box input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .video-item {
            padding: 15px 20px;
            cursor: pointer;
            border-bottom: 1px solid #f0f0f0;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }
        
        body.mobile .video-item {
            padding: 12px 15px;
            font-size: 14px;
        }
        
        .video-item::before {
            content: '▶';
            font-size: 12px;
            color: #667eea;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        body.mobile .video-item::before {
            opacity: 1;
            font-size: 10px;
        }
        
        .video-item:hover {
            background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding-left: 25px;
            transform: translateX(5px);
        }
        
        body.mobile .video-item:hover {
            transform: none;
            padding-left: 15px;
        }
        
        .video-item:hover::before { opacity: 1; }
        
        .video-item:active {
            background: rgba(102, 126, 234, 0.2);
        }
        
        .video-item.active {
            background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border-left: 4px solid #667eea;
            font-weight: 600;
            color: #667eea;
        }
        
        .video-name {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 14px;
        }
        
        #main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px;
            gap: 20px;
        }
        
        body.mobile #main {
            padding: 15px;
            padding-bottom: calc(40vh + 15px);
            height: 100vh;
            overflow-y: auto;
        }
        
        .player-container {
            background: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            max-width: 90%;
            backdrop-filter: blur(10px);
        }
        
        body.mobile .player-container {
            width: 100%;
            max-width: 100%;
            padding: 15px;
            border-radius: 10px;
        }
        
        #player {
            width: 100%;
            max-width: 1000px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.4);
        }
        
        body.mobile #player {
            max-width: 100%;
            border-radius: 8px;
        }
        
        .video-title {
            color: white;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-top: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            max-width: 1000px;
        }
        
        body.mobile .video-title {
            font-size: 16px;
            margin-top: 10px;
            padding: 0 10px;
        }
        
        .empty-state {
            color: white;
            font-size: 18px;
            text-align: center;
            opacity: 0.8;
        }
        
        body.mobile .empty-state {
            font-size: 16px;
            padding: 20px;
        }
        
        /* 可滚动内容容器 */
        .scrollable-content {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
        }
        
        body.mobile .scrollable-content {
            display: flex;
            flex-direction: column;
        }
        
        .video-count {
            padding: 10px 20px;
            background: rgba(102, 126, 234, 0.1);
            text-align: center;
            font-size: 13px;
            color: #667eea;
            font-weight: 500;
            flex-shrink: 0;
        }
        
        body.mobile .video-count {
            padding: 8px 15px;
            font-size: 12px;
            flex-shrink: 0;
        }
        
        .search-box {
            padding: 15px;
            background: white;
            border-bottom: 1px solid #e0e0e0;
        }
        
        body.mobile .search-box {
            padding: 10px 15px;
        }
        
        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s;
        }
        
        body.mobile .search-box input {
            padding: 8px 12px;
            font-size: 13px;
        }
        
        /* 全屏播放按钮 */
        .fullscreen-btn {
            display: none;
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.6);
            color: white;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            font-size: 20px;
            cursor: pointer;
            z-index: 10;
            backdrop-filter: blur(5px);
        }
        
        body.mobile .fullscreen-btn {
            display: block;
        }
        
        .fullscreen-btn:active {
            background: rgba(0,0,0,0.8);
        }
        
        /* 全页面播放按钮 */
        .fullpage-btn {
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 15px;
            padding: 6px 12px;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            backdrop-filter: blur(5px);
            user-select: none;
            transition: all 0.3s ease;
        }
        
        body.mobile .fullpage-btn {
            padding: 5px 10px;
            font-size: 11px;
            gap: 4px;
        }
        
        .fullpage-btn:hover {
            background: rgba(255,255,255,0.25);
        }
        
        .fullpage-btn:active {
            background: rgba(255,255,255,0.3);
        }
        
        .fullpage-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
        }
        
        .fullpage-icon {
            font-size: 12px;
        }
        
        body.mobile .fullpage-icon {
            font-size: 11px;
        }
        
        /* 按钮容器 */
        .controls-container {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            position: relative;
            z-index: 10;
        }
        
        body.mobile .controls-container {
            gap: 8px;
        }
        
        /* 全页面播放模式样式 */
        body.fullpage-mode #sidebar {
            display: none;
        }
        
        body.fullpage-mode #main {
            padding: 0;
        }
        
        body.fullpage-mode .player-container {
            max-width: 100%;
            width: 100%;
            height: 100vh;
            border-radius: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: #000;
            position: relative;
        }
        
        body.fullpage-mode #player {
            max-width: 100%;
            width: 100%;
            height: 100%;
            border-radius: 0;
            object-fit: contain;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
        }
        
        body.fullpage-mode .video-title {
            display: none;
        }
        
        body.fullpage-mode .controls-container {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 100;
            margin-bottom: 0;
        }
        
        /* 连续播放按钮 */
        .autoplay-btn {
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 15px;
            padding: 6px 12px;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            backdrop-filter: blur(5px);
            user-select: none;
            transition: all 0.3s ease;
            min-width: 100px;
        }
        
        body.mobile .autoplay-btn {
            padding: 5px 10px;
            font-size: 11px;
            gap: 4px;
            min-width: 90px;
        }
        
        .autoplay-btn:hover {
            background: rgba(255,255,255,0.25);
        }
        
        .autoplay-btn:active {
            background: rgba(255,255,255,0.3);
        }
        
        .autoplay-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
        }
        
        .autoplay-icon {
            font-size: 12px;
        }
        
        body.mobile .autoplay-icon {
            font-size: 11px;
        }
    </style>
</head>
<body class="{{ 'mobile' if is_mobile else 'desktop' }}">
    <div id="main">
        <button class="fullscreen-btn" id="fullscreenBtn" onclick="toggleFullscreen()">⛶</button>
        <div class="player-container" id="playerContainer" style="display: none;">
            <div class="controls-container">
                <button class="autoplay-btn" id="autoplayBtn" onclick="toggleAutoplay()">
                    <span class="autoplay-icon">🔁</span>
                    <span id="autoplayText">Autoplay</span>
                </button>
                <button class="fullpage-btn" id="fullpageBtn" onclick="toggleFullpage()">
                    <span class="fullpage-icon">⬜</span>
                    <span id="fullpageText">Fullpage</span>
                </button>
            </div>
            <video id="player" controls playsinline webkit-playsinline></video>
            <div class="video-title" id="videoTitle"></div>
        </div>
        <div class="empty-state" id="emptyState">
            <div>🎬</div>
            <div style="margin-top: 10px;">Please select a video to play</div>
        </div>
    </div>
    <div id="sidebar">
        <div class="sidebar-header" id="sidebarHeader">
            <span id="libraryTitle">{{ '🔒 Secret Library' if is_secret_mode else '🎬 Video Library' }}</span>
            <span class="toggle-icon">▼</span>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search videos..." />
        </div>
        <div class="scrollable-content">
            <div class="video-count" id="videoCount">Loading...</div>
            <div id="videoList"></div>
        </div>
    </div>
    
    <!-- Password input dialog -->
    <div id="passwordModal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 10000; align-items: center; justify-content: center;">
        <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 50px rgba(0,0,0,0.5); max-width: 400px; width: 90%;">
            <h2 style="margin: 0 0 20px 0; color: #667eea; text-align: center;">🔐 Secret Space</h2>
            <p style="margin: 0 0 20px 0; color: #666; text-align: center;">Please enter access password</p>
            <input type="password" id="passwordInput" placeholder="Enter password" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box;" />
            <div style="display: flex; gap: 10px;">
                <button onclick="cancelPassword()" style="flex: 1; padding: 12px; background: #ccc; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer;">Cancel</button>
                <button onclick="verifyPassword()" style="flex: 1; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer;">Confirm</button>
            </div>
        </div>
    </div>
    
<script>
const videoListEl = document.getElementById('videoList');
const player = document.getElementById('player');
const playerContainer = document.getElementById('playerContainer');
const emptyState = document.getElementById('emptyState');
const videoTitle = document.getElementById('videoTitle');
const searchInput = document.getElementById('searchInput');
const videoCount = document.getElementById('videoCount');
const sidebar = document.getElementById('sidebar');
const sidebarHeader = document.getElementById('sidebarHeader');
const passwordModal = document.getElementById('passwordModal');
const passwordInput = document.getElementById('passwordInput');
const isMobile = document.body.classList.contains('mobile');
const isSecretMode = {{ 'true' if is_secret_mode else 'false' }};
let currentVideo = null;
let allVideos = [];
let isAutoplayEnabled = false;
let isFullpageMode = false;

// Get URL parameters
const urlParams = new URLSearchParams(window.location.search);
const secretToken = urlParams.get('secretnumber') || '';

// If in secret mode, listen for page refresh events
if (isSecretMode) {
    // Detect if page is refreshed (not first load)
    const pageAccessedByReload = (
        (window.performance.navigation && window.performance.navigation.type === 1) ||
        window.performance
            .getEntriesByType('navigation')
            .map((nav) => nav.type)
            .includes('reload')
    );
    
    if (pageAccessedByReload) {
        // Page refreshed, notify server to invalidate token
        fetch('/invalidate-token?secretnumber=' + secretToken, {method: 'POST'});
    }
    
    // Listen for beforeunload event
    window.addEventListener('beforeunload', function() {
        // Use sendBeacon to ensure request is sent
        navigator.sendBeacon('/invalidate-token?secretnumber=' + secretToken);
    });
}

// Load video list
const videosUrl = secretToken ? '/videos?secretnumber=' + secretToken : '/videos';
fetch(videosUrl).then(r => r.json()).then(list => {
    allVideos = list;
    renderVideoList(list);
    videoCount.textContent = `Total ${list.length} videos`;
    
    // Auto-load last played video (use different key for secret mode)
    const storageKey = isSecretMode ? 'lastSecretVideo' : 'lastVideo';
    const lastVideo = localStorage.getItem(storageKey);
    if (lastVideo && list.includes(lastVideo)) loadVideo(lastVideo);
    
    // Restore autoplay state
    const autoplayKey = isSecretMode ? 'autoplaySecretEnabled' : 'autoplayEnabled';
    const savedAutoplay = localStorage.getItem(autoplayKey);
    if (savedAutoplay === 'true') {
        isAutoplayEnabled = true;
        updateAutoplayButton();
    }
    
    // Restore fullpage mode state
    if (lastVideo && list.includes(lastVideo)) {
        restoreFullpageMode();
    }
});

function renderVideoList(list) {
    videoListEl.innerHTML = '';
    list.forEach(v => {
        const div = document.createElement('div');
        div.className = 'video-item';
        div.innerHTML = `<span class="video-name" title="${v}">${v}</span>`;
        div.onclick = () => loadVideo(v);
        if (v === currentVideo) div.classList.add('active');
        videoListEl.appendChild(div);
    });
}

function loadVideo(v) {
    currentVideo = v;
    const videoUrl = secretToken ? 
        '/video/' + encodeURIComponent(v) + '?secretnumber=' + secretToken : 
        '/video/' + encodeURIComponent(v);
    
    player.src = videoUrl;
    videoTitle.textContent = v;
    
    // Use different storage key
    const storageKey = isSecretMode ? 'lastSecretVideo' : 'lastVideo';
    const timeKey = isSecretMode ? 'secretVideoTime_' + v : 'videoTime_' + v;
    
    localStorage.setItem(storageKey, v);
    player.currentTime = parseFloat(localStorage.getItem(timeKey)) || 0;
    
    playerContainer.style.display = 'block';
    emptyState.style.display = 'none';
    
    // Update selected state
    document.querySelectorAll('.video-item').forEach(item => {
        item.classList.remove('active');
        if (item.querySelector('.video-name').textContent === v) {
            item.classList.add('active');
        }
    });
    
    // Mobile sidebar no longer auto-collapses
    // if (isMobile) {
    //     sidebar.classList.add('collapsed');
    // }
    
    // Restore fullpage mode state
    restoreFullpageMode();
    
    player.play();
}

// Record playback progress
player.ontimeupdate = function() {
    if (currentVideo) {
        const timeKey = isSecretMode ? 'secretVideoTime_' + currentVideo : 'videoTime_' + currentVideo;
        localStorage.setItem(timeKey, player.currentTime);
    }
};

// Video ended event
player.onended = function() {
    if (isAutoplayEnabled && allVideos.length > 0) {
        // Find current video index
        const currentIndex = allVideos.indexOf(currentVideo);
        if (currentIndex !== -1 && currentIndex < allVideos.length - 1) {
            // Play next video
            loadVideo(allVideos[currentIndex + 1]);
        } else if (currentIndex === allVideos.length - 1) {
            // If last video, loop to first
            loadVideo(allVideos[0]);
        }
    }
};

// Toggle autoplay state
function toggleAutoplay() {
    isAutoplayEnabled = !isAutoplayEnabled;
    updateAutoplayButton();
    
    // Save state to localStorage
    const autoplayKey = isSecretMode ? 'autoplaySecretEnabled' : 'autoplayEnabled';
    localStorage.setItem(autoplayKey, isAutoplayEnabled.toString());
}

// Update autoplay button state
function updateAutoplayButton() {
    const btn = document.getElementById('autoplayBtn');
    const text = document.getElementById('autoplayText');
    
    if (isAutoplayEnabled) {
        btn.classList.add('active');
        text.textContent = 'Autoplay: ON';
    } else {
        btn.classList.remove('active');
        text.textContent = 'Autoplay: OFF';
    }
}

// Search functionality
searchInput.addEventListener('input', function() {
    const keyword = this.value.toLowerCase();
    
    // Detect if trigger word is entered
    if (keyword === 'secret' && !isSecretMode) {
        // Show password dialog
        passwordModal.style.display = 'flex';
        passwordInput.value = '';
        passwordInput.focus();
        // Clear search box
        this.value = '';
        return;
    }
    
    const filtered = allVideos.filter(v => v.toLowerCase().includes(keyword));
    renderVideoList(filtered);
    videoCount.textContent = `${filtered.length} / ${allVideos.length} videos`;
});

// Password verification
function verifyPassword() {
    const password = passwordInput.value;
    
    fetch('/verify-secret', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            // Password correct, redirect to secret space
            window.location.href = '/?secretnumber=' + data.token;
        } else {
            alert('Wrong password!');
            passwordInput.value = '';
            passwordInput.focus();
        }
    })
    .catch(err => {
        alert('Verification failed, please try again');
    });
}

// Cancel password input
function cancelPassword() {
    passwordModal.style.display = 'none';
    passwordInput.value = '';
}

// Submit password on Enter key
passwordInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        verifyPassword();
    }
});

// Keyboard shortcuts (desktop only)
if (!isMobile) {
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT') return;
        
        // Prevent keyboard repeat (when holding key)
        if (e.repeat) return;
        
        if (e.key === ' ') {
            e.preventDefault();
            if (player.paused) player.play();
            else player.pause();
        }
        
        // F key toggles fullpage mode
        if (e.key === 'f' || e.key === 'F') {
            e.preventDefault();
            if (currentVideo) {
                toggleFullpage();
            }
        }
        
        // Esc key exits fullpage mode
        if (e.key === 'Escape' && isFullpageMode) {
            e.preventDefault();
            toggleFullpage();
        }
    });
}

// Mobile sidebar toggle
if (isMobile) {
    sidebarHeader.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
    });
    
    // No longer auto-collapse on initialization
    // setTimeout(() => {
    //     if (!currentVideo) {
    //         sidebar.classList.add('collapsed');
    //     }
    // }, 2000);
}

// Fullscreen functionality
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        if (player.requestFullscreen) {
            player.requestFullscreen();
        } else if (player.webkitRequestFullscreen) {
            player.webkitRequestFullscreen();
        } else if (player.webkitEnterFullscreen) {
            player.webkitEnterFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
    }
}

// Fullpage mode functionality
function toggleFullpage() {
    isFullpageMode = !isFullpageMode;
    updateFullpageButton();
    
    // Save state
    const storageKey = isSecretMode ? 'fullpageSecretMode' : 'fullpageMode';
    localStorage.setItem(storageKey, isFullpageMode.toString());
}

// Update fullpage button state
function updateFullpageButton() {
    const btn = document.getElementById('fullpageBtn');
    const icon = document.querySelector('.fullpage-icon');
    const text = document.getElementById('fullpageText');
    
    if (isFullpageMode) {
        document.body.classList.add('fullpage-mode');
        btn.classList.add('active');
        icon.textContent = '◱';
        text.textContent = 'Fullpage: ON';
    } else {
        document.body.classList.remove('fullpage-mode');
        btn.classList.remove('active');
        icon.textContent = '⬜';
        text.textContent = 'Fullpage: OFF';
    }
}

// Restore fullpage mode state
function restoreFullpageMode() {
    const storageKey = isSecretMode ? 'fullpageSecretMode' : 'fullpageMode';
    const savedFullpage = localStorage.getItem(storageKey);
    if (savedFullpage === 'true' && currentVideo) {
        isFullpageMode = true;
        updateFullpageButton();
    }
}

// Prevent double-tap zoom on mobile
if (isMobile) {
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function(e) {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) {
            e.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
}
</script>
</body>
</html>
''', is_mobile=is_mobile, is_secret_mode=is_secret_mode)

# Verify password and generate token
@app.route('/verify-secret', methods=['POST'])
def verify_secret():
    data = request.get_json()
    password = data.get('password', '')
    
    if password == SECRET_PASSWORD:
        # Generate unique token
        token = secrets.token_urlsafe(32)
        # Set token validity to 5 minutes (user has 5 minutes to click the link)
        valid_tokens[token] = time.time() + 300
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False})

# Invalidate token
@app.route('/invalidate-token', methods=['POST'])
def invalidate_token():
    secret_token = request.args.get('secretnumber', '')
    if secret_token and secret_token in valid_tokens:
        del valid_tokens[secret_token]
    return '', 204

@app.route('/videos')
def videos():
    # Check if in secret mode
    secret_token = request.args.get('secretnumber', '')
    is_secret = False
    
    if secret_token and secret_token in valid_tokens:
        # Token exists means it's valid (including used state -1)
        is_secret = True
    
    return jsonify(get_video_list(is_secret=is_secret))

@app.route('/video/<path:filename>')
def video(filename):
    # Check if in secret mode
    secret_token = request.args.get('secretnumber', '')
    is_secret = False
    
    if secret_token and secret_token in valid_tokens:
        # Token exists means it's valid (including used state -1)
        is_secret = True
    
    video_root = SECRET_VIDEO_ROOT if is_secret else VIDEO_ROOT
    file_path = os.path.join(video_root, filename)
    
    if not os.path.isfile(file_path):
        return 'File not found', 404

    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(file_path)

    size = os.path.getsize(file_path)
    byte1, byte2 = 0, size - 1
    m = range_header.replace('bytes=', '').split('-')
    if m[0]: byte1 = int(m[0])
    if m[1]: byte2 = int(m[1])
    length = byte2 - byte1 + 1

    with open(file_path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    # Set correct MIME type based on file extension
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.ogg': 'video/ogg',
        '.mkv': 'video/x-matroska',
        '.rmvb': 'application/vnd.rn-realmedia-vbr',
        '.avi': 'video/x-msvideo',
        '.flv': 'video/x-flv',
        '.mov': 'video/quicktime'
    }
    mimetype = mime_types.get(ext, 'video/mp4')
    
    resp = app.response_class(data, 206, mimetype=mimetype, direct_passthrough=True)
    resp.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{size}')
    resp.headers.add('Accept-Ranges', 'bytes')
    resp.headers.add('Content-Length', str(length))
    return resp

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)

