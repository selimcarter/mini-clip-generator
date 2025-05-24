from moviepy.editor import VideoFileClip
import os

def extract_clips(video_path, segments):
    clips = []
    video = VideoFileClip(video_path)
    for i, (start, end) in enumerate(segments):
        clip = video.subclip(start, end)
        output_path = f"clip_{i}.mp4"
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
        clips.append(output_path)
    return clips