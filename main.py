from audio.audio_extractor import extract_audio_from_video
from audio.audio_transcriber import AudioTranscriber
from download.youtube_downloader import YouTubeDownloader
from frame_to_caption import FrameToCaption
from llm_chat import LLMChat
from video_to_frames import VideoFrameExtractor
import os
youtube_url = "https://www.youtube.com/watch?v=wXFQ-ibAIIM"

import uuid

id = uuid.uuid4()
working_dir = f"./working_dir/{id}"
frame_dir = "./frames"
audio_path = "./audio.mp3"
LLM_MODEL="mistral"

os.makedirs(working_dir, exist_ok=True)
os.chdir(working_dir)

downloader = YouTubeDownloader(youtube_url, ".")
video_path = downloader.run()
videoFrameExtractor = VideoFrameExtractor(video_path, frame_dir)
frames = videoFrameExtractor.extract_frames()

extract_audio_from_video(video_path, audio_path)

audio_transcriber = AudioTranscriber(audio_path)
transcript =audio_transcriber.run()

captions = FrameToCaption().caption_frames("./frames")

prompt = {
    "role": "user",
    "content": f"""Summarize this video based on the provided speech and visual information:

Speech: {transcript}
Visual: {captions}
"""
}

response = LLMChat(model=LLM_MODEL).ask([prompt])
print(response)