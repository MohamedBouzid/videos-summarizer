# Video Summarizer Frontend

A React TypeScript frontend for the Video Summarizer application that exposes the Python video summarization functionality through a web interface.

## Features

- Enter a YouTube video URL to summarize
- Real-time processing status updates
- Display of video summary, transcript, and frame captions
- Modern, responsive UI design
- TypeScript for type safety

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Python backend running (see main project README)

## Installation

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

### Option 1: Run Frontend and Backend Separately

1. Start the Python backend (from the project root):
```bash
python api.py
```

2. In a new terminal, start the React frontend:
```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000` and will proxy API requests to the backend at `http://localhost:5000`.

### Option 2: Using the Start Script

From the project root, run:
```bash
start_app.bat
```

This will start both the backend and frontend in separate windows.

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a YouTube video URL in the input field
3. Click "Summarize Video"
4. Wait for the processing to complete (this may take several minutes depending on video length)
5. View the generated summary, transcript, and frame captions

## API Endpoints

The frontend communicates with the following backend endpoints:

- `POST /api/summarize` - Start video summarization
- `GET /api/status/<job_id>` - Check processing status
- `GET /api/health` - Health check

## Technologies Used

- React 18
- TypeScript
- Axios for HTTP requests
- CSS3 with modern styling
- Flask backend (Python)

## TypeScript

This project uses TypeScript for type safety. Key interfaces:

- `JobResult` - Contains summary, transcript, and captions
- `JobStatus` - Contains status, message, and result

Type definitions are automatically installed via `@types/react` and `@types/react-dom`.
