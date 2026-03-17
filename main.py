from video_downloader import VideoDownloader
from youtube_downloader import YouTubeDownloader

youtube_url = "https://www.youtube.com/watch?v=cSkoaCCmq0w"
downloader = YouTubeDownloader(youtube_url, ".")
downloader.run()