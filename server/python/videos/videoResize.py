import moviepy.editor as mp
import os

if not os.path.exists("./resizedVideos"):
    os.mkdir("./resizedVideos")

clip = mp.VideoFileClip("./input.mp4")
for height in [16,32,64,128]:
    clip_resized = clip.resize(height=height) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
    clip_resized.write_videofile("./resizedVideos/{}.mp4".format(height))