
from audio.audio_extractor import extract_audio_from_video
from audio.audio_transcriber import AudioTranscriber
from download.youtube_downloader import YouTubeDownloader
from video_to_frames import VideoFrameExtractor

youtube_url = "https://www.youtube.com/watch?v=cSkoaCCmq0w"
downloader = YouTubeDownloader(youtube_url, ".")
video_path = downloader.run()

videoFrameExtractor = VideoFrameExtractor(video_path, "./frames")
videoFrameExtractor.extract_frames()

audio_path = "./audio.mp3"
extract_audio_from_video(video_path, audio_path)

audio_transcriber = AudioTranscriber(audio_path)
transcript =audio_transcriber.run()

