import yt_dlp

from audio.video_downloader import VideoDownloader



class YouTubeDownloader(VideoDownloader):

    def __init__(self, video_url, path):
        super().__init__(video_url, path)

    def do_run(self):
        file_name = 'video.mp4'
        ydl_opts = {
            'outtmpl': file_name
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])
        return self.path + "/" + file_name