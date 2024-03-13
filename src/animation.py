import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# This needs to be changed for your code
# plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\spsha\\Desktop\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe'

# This is the final example I showed in the code - notice I have 2 "cursor marks" not shown in the video
fig = plt.figure()
l, = plt.plot([], [], 'k-')
l2, = plt.plot([], [], 'm--')
p1, = plt.plot([], [], 'ko')
p2, = plt.plot([], [], 'mo')

plt.xlabel('xlabel')
plt.ylabel('ylabel')
plt.title('title')

plt.xlim(-5, 5)
plt.ylim(-5, 5)

def func(x):
    return np.sin(x)*3

def func2(x):
    return np.cos(x)*3

metadata = dict(title='Movie', artist='codinglikemad')
writer = PillowWriter(fps=15, metadata=metadata)


xlist = []
xlist2 = []
ylist = []
ylist2 = []

with writer.saving(fig, "sinWave2.gif", 100):
    for xval in np.linspace(-5, 5, 100):
        xlist.append(xval)
        ylist.append(func(xval))

        l.set_data(xlist, ylist)
        writer.grab_frame()
    