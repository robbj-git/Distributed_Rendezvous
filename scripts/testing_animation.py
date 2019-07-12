import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation

fig, ax = plt.subplots()
xdata, ydata = [], []
line, = plt.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return line,

def update(data):
    xdata.append(data)
    ydata.append(2*data)
    line.set_data(xdata, ydata)
    return line,

animation = FuncAnimation(fig, update, frames=[1, 2, 3, 4, 5], init_func=init, blit=True)

# Set up formatting for the movie files
Writer = matplotlib.animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

animation.save('test_anim.mp4', writer=writer)

print "should have saved"
# plt.show()
