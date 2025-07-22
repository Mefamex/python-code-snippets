#import subprocess; subprocess.run(['ffmpeg', '-i', 'a.mp4', '-vf', 'scale=-1:1080', 'movie_resized.mp4'])

############### ALTERNATIVE METHOD USING MOVIEPY ####################

from moviepy.video.io.VideoFileClip import VideoFileClip

clip = VideoFileClip("a.mp4")

# make the height 360px
clip.resized(height=720)

clip.write_videofile("movie_resized.mp4")
clip.close()


############## ANOTHER WAY USING MOVIEPY ####################

""" ANOTHER WAY
import moviepy.editor as mp

clip = mp.VideoFileClip("a.mp4")

# make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
clip_resized = clip.resize(height=720)

clip_resized.write_videofile("movie_resized.mp4")
"""