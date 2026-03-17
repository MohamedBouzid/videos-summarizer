import cv2
import os

class VideoFrameExtractor:
    def __init__(self, video_path, output_dir):
        self.video_path = video_path
        self.output_dir = output_dir

    def extract_frames(self):

        print(f"Extracting frames from {self.video_path}...")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        cap = cv2.VideoCapture(self.video_path)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Save the frame as an image file
            frame_filename = os.path.join(self.output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        # Release the video capture object
        cap.release()
        print(f"Frame extraction is done. {frame_count} frames extracted to {self.output_dir}.")