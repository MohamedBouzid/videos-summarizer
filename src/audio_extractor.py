from moviepy import VideoFileClip

def extract_audio_from_video(video_path, audio_path):
    print(f"Extracting audio from {video_path}...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extraction is done {video_path}...")
