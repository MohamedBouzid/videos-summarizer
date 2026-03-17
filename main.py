from audio_extractor import extract_audio_from_video
from audio_transcriber import AudioTranscriber
from video_downloader import VideoDownloader
from youtube_downloader import YouTubeDownloader

youtube_url = "https://www.youtube.com/watch?v=cSkoaCCmq0w"
downloader = YouTubeDownloader(youtube_url, ".")
video_path = downloader.run()

audio_path = "./audio.mp3"
extract_audio_from_video(video_path, audio_path)

audio_transcriber = AudioTranscriber(audio_path)
transcript =audio_transcriber.run()
