#!/usr/bin/env python3
"""
Simple Video Share Server
A lightweight video sharing server for LAN environments
"""

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import cgi
from pathlib import Path

# Configuration
UPLOAD_DIR = "videos"
PORT = 8000

class VideoShareHandler(SimpleHTTPRequestHandler):
    """Custom handler for video sharing functionality"""
    
    def __init__(self, *args, **kwargs):
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/videos':
            self.send_video_list()
            return
        
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for video uploads"""
        if self.path == '/api/upload':
            self.handle_upload()
        else:
            self.send_error(404, "Not Found")
    
    def send_video_list(self):
        """Send list of available videos"""
        videos = []
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                if filename.lower().endswith(('.mp4', '.webm', '.ogg', '.mov', '.avi')):
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    stat = os.stat(filepath)
                    videos.append({
                        'name': filename,
                        'url': f'/{UPLOAD_DIR}/{filename}',
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    })
        
        # Sort by modification time (newest first)
        videos.sort(key=lambda x: x['modified'], reverse=True)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(videos).encode())
    
    def handle_upload(self):
        """Handle video file upload"""
        try:
            content_type = self.headers['Content-Type']
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Bad Request: Expected multipart/form-data")
                return
            
            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )
            
            if 'video' not in form:
                self.send_error(400, "Bad Request: No video file provided")
                return
            
            file_item = form['video']
            if not file_item.filename:
                self.send_error(400, "Bad Request: No filename provided")
                return
            
            # Save the file
            filename = os.path.basename(file_item.filename)
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            with open(filepath, 'wb') as f:
                f.write(file_item.file.read())
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'success': True,
                'message': 'Video uploaded successfully',
                'filename': filename
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

def run_server(port=PORT):
    """Start the video share server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, VideoShareHandler)
    print(f"🎬 Simple Video Share Server")
    print(f"📡 Server running at http://localhost:{port}/")
    print(f"📂 Videos stored in: {os.path.abspath(UPLOAD_DIR)}/")
    print(f"🌐 Access from other devices using your local IP address")
    print(f"⏹  Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
