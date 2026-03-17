from faster_whisper import WhisperModel

class AudioTranscriber:
    
    model = WhisperModel("base", device="cpu")

    def __init__(self, audio_path):
        self.audio_path = audio_path

    def run(self) -> str:
        print(f"Transcribing audio from {self.audio_path}...")
        segments, info = self.model.transcribe(self.audio_path)
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "
        return transcript