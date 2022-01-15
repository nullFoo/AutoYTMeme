import os
from moviepy.editor import *
import praw
import requests
import urllib.request
import glob

def logStr(string):
    print("")
    print("=================================")
    print(string)
    print("=================================")
    print("")

def getVideos(amount):
    logStr("Getting videos from Reddit")
    reddit = praw.Reddit(client_id='JN1Od4POfxHFLw',
                     client_secret='MULo2NdZ9jPID9PDeI8cL01mTaQ',
                     user_agent='reddit->discord bot')

    subs = ["funny"]
    posts = []
    for sub in subs:
        posts += list(reddit.subreddit(sub).new(limit=30))

    videoLinks = []
    for post in posts:
        if(post.is_video):
            if(post.media['reddit_video']['duration'] < 30):
                fallback_url = post.media['reddit_video']['fallback_url']
                videoLinks.append(fallback_url)

        if(len(videoLinks) > amount):
            break

    logStr("Combining video with audio and saving")
    for vid in range(len(videoLinks)):
        try:
            videoLink = videoLinks[vid]
            urllib.request.urlretrieve(
                videoLink,
                filename="tmp/video"+str(vid)+".mp4",
            )
            audioLink = videoLink.split("DASH_")[0] + "DASH_audio.mp4" + videoLink.split(".mp4")[1]
            urllib.request.urlretrieve(
                audioLink,
                filename="tmp/audio"+str(vid)+".mp4",
            )

            clip = VideoFileClip("tmp/video"+str(vid)+".mp4")

            h = AudioFileClip("tmp/audio"+str(vid)+".mp4")
            h.write_audiofile("tmp/video"+str(vid)+".mp3")
            audioclip = AudioFileClip("tmp/video"+str(vid)+".mp3")

            videoclip = clip.set_audio(audioclip)

            videoclip.write_videofile("input/output"+str(vid)+".mp4")
        except:
            pass
def combineVideos():
    logStr("Combining into compilation")
    clips = []
    for filename in os.listdir("input"):
        if filename.endswith(".mp4") and filename.startswith("output"):
            print(filename)
            clips.append(VideoFileClip("input/"+filename))

    final_clip = concatenate_videoclips(clips,method='compose')
    final_clip.write_videofile("final_output.mp4",fps=24)

def clearTmp():
    logStr("Clearing temporary files")
    files = glob.glob("tmp/*")
    for f in files:
        os.remove(f)

def clearInput():
    logStr("Clearing temporary files")
    files = glob.glob("input/*")
    for f in files:
        os.remove(f)

getVideos(int(input("How many videos to scrape? (maximum)")))
clearTmp()
combineVideos()
clearInput()
logStr("Done!")
