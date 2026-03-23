import os
import cv2

class VideoFrameExtractor:
    def __init__(self, video_path, output_dir):
        self.video_path = video_path
        self.output_dir = output_dir

    def extract_frames(self, seconds_interval=2):
        print(f"Extracting frames from {self.video_path}...")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        cap = cv2.VideoCapture(self.video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps * seconds_interval)  # number of frames to skip

        frames = []
        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Save only every 'interval' frames
            if frame_count % interval == 0:
                frame_filename = os.path.join(
                    self.output_dir, f"frame_{saved_count:04d}.jpg"
                )
                cv2.imwrite(frame_filename, frame)
                frames.append(frame_filename)
                saved_count += 1

            frame_count += 1

        cap.release()

        print(f"Done. {saved_count} frames extracted every {seconds_interval} seconds.")
        return frames