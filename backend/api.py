from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import threading
from src.audio.audio_extractor import extract_audio_from_video
from src.download.youtube_downloader import YouTubeDownloader
from src.frame_to_caption import FrameToCaption
from src.llm_chat import LLMChat
from src.audio.audio_transcriber import AudioTranscriber
from src.video_to_frames import VideoFrameExtractor

app = Flask(__name__)
CORS(app)

# Store for tracking job status
jobs = {}

def process_video(job_id, youtube_url):
    """Process video in a background thread"""
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Starting video processing...'
        
        # Create working directory
        working_dir = f"./working_dir/{job_id}"
        frame_dir = "./frames"
        audio_path = "./audio.mp3"
        LLM_MODEL = "mistral"
        
        os.makedirs(working_dir, exist_ok=True)
        original_dir = os.getcwd()
        os.chdir(working_dir)
        
        try:
            # Download video
            jobs[job_id]['message'] = 'Downloading video...'
            downloader = YouTubeDownloader(youtube_url, ".")
            video_path = downloader.run()
            
            # Extract frames
            jobs[job_id]['message'] = 'Extracting frames...'
            videoFrameExtractor = VideoFrameExtractor(video_path, frame_dir)
            frames = videoFrameExtractor.extract_frames()
            
            # Extract audio
            jobs[job_id]['message'] = 'Extracting audio...'
            extract_audio_from_video(video_path, audio_path)
            
            # Transcribe audio
            jobs[job_id]['message'] = 'Transcribing audio...'
            audio_transcriber = AudioTranscriber(audio_path)
            transcript = audio_transcriber.run()
            
            # Caption frames
            jobs[job_id]['message'] = 'Captioning frames...'
            captions = FrameToCaption().caption_frames("./frames")
            llm_chat = LLMChat(model=LLM_MODEL)
            removedulication_captions = list(set(captions))

            prompt = {
                "role": "user",
                "content": f"""Summarize the captions of the video frames and remove repetitions:
                 Visual: {removedulication_captions}
                """
            }
            print("Captions for summarization: " + str(removedulication_captions))
            response = llm_chat.ask([prompt])
            print("Summarized captions: " + response['message']['content'])
            resumed_captions = response['message']['content']
            # Generate summary
            jobs[job_id]['message'] = 'Generating summary...'
            prompt = {
                "role": "user",
                "content": f"""Summarize this video based on the provided transcript and the captions of the video frames; try to make a link between the transcript and the captions to generate a more comprehensive summary and DON'T summurize the transcript and the captions separately, but try to combine them together in a way that makes sense:
                Speech: {transcript}
                Visual: {resumed_captions}
                """
            }
            
            response = llm_chat.ask([prompt])
            
            # Extract the summary from response
            summary = response['message']['content']
            print("Summarized captions: " + response['message']['content'])

            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['message'] = 'Video processing completed'
            jobs[job_id]['result'] = {
                'summary': summary,
                'transcript': transcript,
                'captions': resumed_captions
            }
            
        finally:
            os.chdir(original_dir)
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f'Error: {str(e)}'

@app.route('/api/summarize', methods=['POST'])
def summarize_video():
    """Start video summarization process"""
    print("Received request to summarize video")
    data = request.get_json()
    
    if not data or 'youtube_url' not in data:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    youtube_url = data['youtube_url']
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    jobs[job_id] = {
        'status': 'queued',
        'message': 'Job queued',
        'result': None
    }
    
    # Start processing in background thread
    thread = threading.Thread(target=process_video, args=(job_id, youtube_url))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Video processing started'
    })

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get the status of a video processing job"""
    print("Received request for job status: ")
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
