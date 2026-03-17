from abc import abstractmethod
from pathlib import Path
import os

class VideoDownloader:
    def __init__(self, video_url, path=None):
        self.video_url = video_url
        self.path = path

    def run(self):
        # Placeholder for the actual download logic
        print(f"Downloading video from {self.video_url}...")

        project_dir = Path(self.path)
        os.chdir(project_dir)

        video_path = self.do_run()
        print("Download complete!")
        return video_path

    @abstractmethod
    def do_run(self):
        pass