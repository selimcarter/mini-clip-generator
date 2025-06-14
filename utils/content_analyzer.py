import whisper

def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["text"]

def extract_important_segments(text):
    return [(0, 10), (10, 20)]