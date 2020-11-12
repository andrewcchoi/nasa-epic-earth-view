import os
import datetime as dt
import moviepy.video.io.ImageSequenceClip
image_folder = 'images/natural'
fps = 15

beg = dt.datetime.now()

image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith(".png")]
print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('my_video.mp4')

end = dt.datetime.now()
print(beg, end, end - beg, sep='-')