
# Factopia Video Generator API

This is a Flask API that takes a script and a voiceover `.mp3`, and generates a vertical video suitable for YouTube Shorts.

## Endpoint

**POST /generate**

**Request JSON:**
```
{
  "script": "Your text here...",
  "voice_url": "https://yourdomain.com/yourfile.mp3"
}
```

**Response:**
```
{
  "video_url": "https://your-api.onrender.com/static/factopia_short.mp4"
}
```

## Deployment

Deploy to [Render](https://render.com) as a Web Service:

- Python 3.10
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`
