import os
from platform import processor
from transformers import BlipForConditionalGeneration, BlipProcessor
from PIL import Image


class FrameToCaption:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def caption_image(self, path):
        image = Image.open(path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt")
        output = self.model.generate(**inputs)

        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption


    def caption_frames(self, frame_paths):
        print(f"Captioning frames in {frame_paths}...")
        captions = []
        for path in os.listdir(frame_paths):
            caption=self.caption_image(frame_paths + "/" + path)
            print("caption: " + caption)
            captions.append(caption)
        print("Done captioning frames.")
        return captions