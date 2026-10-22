#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/python3
#%%
import matplotlib.pyplot as plt
import numpy as np

#fig, ax = plt.subplots()
t = np.linspace(0, np.pi, 100)
y = np.sin(t)
N = 20
plt.ion()
plt.figure()
plt.plot(t, y)
plt.draw()
#def onclick(event):
#    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#          ('double' if event.dblclick else 'single', event.button,
#           event.x, event.y, event.xdata, event.ydata))
#
#cid = fig.canvas.mpl_connect('button_press_event', onclick)