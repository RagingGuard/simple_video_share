// Simple Video Share - Client Script

// DOM Elements
const videoInput = document.getElementById('videoInput');
const uploadArea = document.getElementById('uploadArea');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const uploadStatus = document.getElementById('uploadStatus');
const videoList = document.getElementById('videoList');
const videoPlayer = document.getElementById('videoPlayer');
const playerContainer = document.getElementById('playerContainer');
const noVideo = document.getElementById('noVideo');
const videoInfo = document.getElementById('videoInfo');
const refreshBtn = document.getElementById('refreshBtn');

// Current playing video
let currentVideo = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadVideos();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // File input change
    videoInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Refresh button
    refreshBtn.addEventListener('click', loadVideos);
    
    // Prevent default drag behavior on document
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => e.preventDefault());
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        uploadVideo(file);
    }
}

// Handle drag over
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

// Handle drag leave
function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

// Handle file drop
function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('video/')) {
            uploadVideo(file);
        } else {
            showStatus('请上传视频文件！', 'error');
        }
    }
}

// Upload video file
async function uploadVideo(file) {
    // Validate file type
    if (!file.type.startsWith('video/')) {
        showStatus('请上传视频文件！', 'error');
        return;
    }
    
    // Show progress
    uploadProgress.classList.remove('hidden');
    uploadStatus.classList.add('hidden');
    progressFill.style.width = '0%';
    progressText.textContent = '上传中... 0%';
    
    // Create form data
    const formData = new FormData();
    formData.append('video', file);
    
    try {
        // Upload with progress tracking
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                progressFill.style.width = percent + '%';
                progressText.textContent = `上传中... ${percent}%`;
            }
        });
        
        xhr.addEventListener('load', () => {
            uploadProgress.classList.add('hidden');
            
            if (xhr.status === 200) {
                showStatus('✅ 视频上传成功！', 'success');
                videoInput.value = ''; // Clear input
                setTimeout(() => {
                    loadVideos(); // Refresh video list
                }, 1000);
            } else {
                showStatus('❌ 上传失败，请重试', 'error');
            }
        });
        
        xhr.addEventListener('error', () => {
            uploadProgress.classList.add('hidden');
            showStatus('❌ 网络错误，上传失败', 'error');
        });
        
        xhr.open('POST', '/api/upload');
        xhr.send(formData);
        
    } catch (error) {
        uploadProgress.classList.add('hidden');
        showStatus('❌ 上传失败: ' + error.message, 'error');
    }
}

// Show status message
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = 'status-message ' + type;
    uploadStatus.classList.remove('hidden');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            uploadStatus.classList.add('hidden');
        }, 5000);
    }
}

// Load video list
async function loadVideos() {
    try {
        videoList.innerHTML = '<div class="loading">加载中...</div>';
        
        const response = await fetch('/api/videos');
        const videos = await response.json();
        
        if (videos.length === 0) {
            videoList.innerHTML = '<div class="no-videos">暂无视频<br>请上传视频文件</div>';
            return;
        }
        
        // Render video list
        videoList.innerHTML = '';
        videos.forEach(video => {
            const videoItem = createVideoItem(video);
            videoList.appendChild(videoItem);
        });
        
    } catch (error) {
        videoList.innerHTML = '<div class="no-videos">加载失败<br>' + error.message + '</div>';
    }
}

// Create video item element
function createVideoItem(video) {
    const item = document.createElement('div');
    item.className = 'video-item';
    item.onclick = () => playVideo(video);
    
    const thumbnail = document.createElement('div');
    thumbnail.className = 'video-thumbnail';
    thumbnail.textContent = '🎬';
    
    const details = document.createElement('div');
    details.className = 'video-details';
    
    const name = document.createElement('div');
    name.className = 'video-name';
    name.textContent = video.name;
    
    const meta = document.createElement('div');
    meta.className = 'video-meta';
    
    const size = document.createElement('span');
    size.className = 'video-size';
    size.textContent = formatFileSize(video.size);
    
    const date = document.createElement('span');
    date.className = 'video-date';
    date.textContent = formatDate(video.modified);
    
    meta.appendChild(size);
    meta.appendChild(date);
    
    details.appendChild(name);
    details.appendChild(meta);
    
    item.appendChild(thumbnail);
    item.appendChild(details);
    
    return item;
}

// Play video
function playVideo(video) {
    currentVideo = video;
    
    // Update player
    videoPlayer.src = video.url;
    videoPlayer.load();
    
    // Show player, hide no-video message
    noVideo.classList.add('hidden');
    videoPlayer.classList.remove('hidden');
    
    // Update video info
    videoInfo.textContent = `正在播放: ${video.name} (${formatFileSize(video.size)})`;
    
    // Start playing
    videoPlayer.play().catch(err => {
        console.error('播放失败:', err);
    });
    
    // Scroll to player
    playerContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format date
function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);
    const now = new Date();
    const diff = now - date;
    
    // Less than 24 hours
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        if (hours === 0) {
            const minutes = Math.floor(diff / 60000);
            return minutes === 0 ? '刚刚' : `${minutes}分钟前`;
        }
        return `${hours}小时前`;
    }
    
    // Less than 7 days
    if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days}天前`;
    }
    
    // Format as date
    return date.toLocaleDateString('zh-CN');
}
