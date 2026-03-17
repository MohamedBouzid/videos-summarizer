import yt_dlp

from video_downloader import VideoDownloader

url = "YOUTUBE_URL"
ydl_opts = {
    'outtmpl': 'video.mp4'
}

class YouTubeDownloader(VideoDownloader):

    def __init__(self, video_url, path):
        super().__init__(video_url, path)

    def do_run(self):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])