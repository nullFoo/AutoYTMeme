import os
from moviepy.editor import *

def getVideos():
    print("Getting")
def combineVideos():
    clips = []
    for filename in os.listdir("input"):
        if filename.endswith(".mp4"):
            print(filename)
            clips.append(VideoFileClip("input/"+filename))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("output.mp4")


getVideos()
combineVideos()
