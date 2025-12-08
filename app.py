import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from config import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_ENV', 'development')])

# Initialize database
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class Video(db.Model):
    """Video model for storing video information."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Video {self.title}>'

# Helper functions
def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_mime_type(filename):
    """Get MIME type based on file extension."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_types = {
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'mkv': 'video/x-matroska',
        'webm': 'video/webm'
    }
    return mime_types.get(ext, 'video/mp4')

# Make get_mime_type available to templates
app.jinja_env.globals.update(get_mime_type=get_mime_type)

# Routes
@app.route('/')
def index():
    """Home page showing all videos."""
    videos = Video.query.order_by(Video.uploaded_at.desc()).all()
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload video page."""
    if request.method == 'POST':
        # Check if file is in request
        if 'video' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['video']
        
        # Check if file is selected
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # Check if file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Save to database
            title = request.form.get('title', filename)
            description = request.form.get('description', '')
            video = Video(title=title, filename=filename, description=description)
            db.session.add(video)
            db.session.commit()
            
            flash('Video uploaded successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Allowed types: mp4, avi, mov, mkv, webm')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/video/<int:video_id>')
def video(video_id):
    """View single video."""
    video = Video.query.get_or_404(video_id)
    return render_template('video.html', video=video)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded videos."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:video_id>', methods=['POST'])
def delete(video_id):
    """Delete a video."""
    video = Video.query.get_or_404(video_id)
    
    # Delete file from filesystem
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Delete from database
    db.session.delete(video)
    db.session.commit()
    
    flash('Video deleted successfully!')
    return redirect(url_for('index'))

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Debug mode is enabled by default for development convenience
    # In production, use a WSGI server (gunicorn, uwsgi) and set FLASK_ENV=production
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode)
