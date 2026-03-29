# Video Summarizer

A multimodal video summarization tool that uses audio transcription, visual frame analysis, and a local LLM to summarize YouTube videos.

## Features

- Download YouTube videos
- Extract and transcribe audio using Whisper
- Extract and caption video frames using BLIP
- Generate comprehensive summaries using a local LLM (Mistral)
- **NEW**: React TypeScript web interface for easy interaction

## Project Structure

```
videos-summarizer/
├── backend/
│   ├── api.py                    # Flask API backend
│   ├── main.py                   # Original CLI script
│   └── src/
│       ├── audio/
│       │   ├── audio_extractor.py
│       │   ├── audio_transcriber.py
│       │   └── video_downloader.py
│       ├── download/
│       │   └── youtube_downloader.py
│       ├── frame_to_caption.py
│       ├── llm_chat.py
│       └── video_to_frames.py
├── frontend/                 # React TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── index.tsx
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── start_app.bat            # Windows startup script
└── pyproject.toml
```

## Prerequisites

- Python 3.10+
- Node.js 14+ (for React frontend)
- Ollama installed and running with Mistral model

## Installation

### Python Backend

1. Create and activate a virtual environment:
```bash
python -m venv .myvenv
.myvenv\Scripts\activate  # Windows
source .myvenv/bin/activate  # Linux/Mac
```

2. Install Python dependencies:
```bash
pip install -e .
```

3. Install Ollama and pull the Mistral model:
```bash
ollama pull mistral
```

### React Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

This will install all required packages including TypeScript and React type definitions.

## Running the Application

### Option 1: Using the Start Script (Windows)

Simply run:
```bash
start_app.bat
```

This will start both the backend and frontend in separate windows.

### Option 2: Manual Start

1. Start the Python backend:
```bash
cd backend
python api.py
```

2. In a new terminal, start the React frontend:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

### Option 3: CLI Mode

For command-line usage, edit the `youtube_url` in `backend/main.py` and run:
```bash
cd backend
python main.py
```

## Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Enter a YouTube video URL
3. Click "Summarize Video"
4. Wait for processing (may take several minutes)
5. View the summary, transcript, and frame captions

### API Endpoints

- `POST /api/summarize` - Start video summarization
  - Body: `{ "youtube_url": "https://www.youtube.com/watch?v=..." }`
  - Returns: `{ "job_id": "...", "status": "queued" }`

- `GET /api/status/<job_id>` - Check processing status
  - Returns: `{ "status": "processing|completed|failed", "message": "...", "result": {...} }`

- `GET /api/health` - Health check

## Technologies

### Backend
- Python 3.10+
- Flask & Flask-CORS
- yt-dlp (YouTube video download)
- faster-whisper (audio transcription)
- OpenCV (frame extraction)
- Transformers & BLIP (image captioning)
- Ollama (local LLM)

### Frontend
- React 18
- TypeScript
- Axios
- CSS3

## Notes

- Video processing time depends on video length and your hardware
- The first run may be slower as models are downloaded
- Ensure Ollama is running before starting the application
- The frontend proxies API requests to the backend at `http://localhost:5000`
- TypeScript provides type safety and better developer experience
