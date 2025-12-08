# Simple Video Share

A lightweight web application for uploading, sharing, and managing videos built with Flask and SQLite.

## Features

- 📤 Upload videos (MP4, AVI, MOV, MKV, WebM)
- 📺 View and play videos in the browser
- 🗑️ Delete videos
- 📝 Add titles and descriptions to videos
- 💾 SQLite database for metadata storage
- 🎨 Clean, responsive UI

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RagingGuard/simple_video_share.git
cd simple_video_share
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Start uploading and sharing videos!

## Configuration

The application can be configured through environment variables or by modifying `config.py`:

- `SECRET_KEY`: Secret key for session management (change in production)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Directory for uploaded videos
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 100MB)

## Project Structure

```
simple_video_share/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── upload.html    # Upload page
│   └── video.html     # Video player page
├── static/            # Static files
│   └── css/
│       └── style.css  # Stylesheet
└── uploads/           # Uploaded videos (created automatically)
```

## Production Deployment

For production deployment:

1. Set environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-key
```

2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

3. **Important**: Never run Flask with `debug=True` in production as it can allow arbitrary code execution.

## License

MIT License