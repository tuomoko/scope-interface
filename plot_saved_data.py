#!/usr/bin/env python2
# -*- coding: utf-8 -*-
u"""Plot the saved trace.

Plots data saved from the scope to the traces/ folder.
By default the script plots the latest trace, but this can be customized by
adding the filename as a command line argument.

@author: Tuomo Kohtamäki
"""
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys

if len(sys.argv) == 1:
    list_of_files = glob.glob('traces/*.npz')
    filename = max(list_of_files)
else:
    filename = sys.argv[1]

saved_data = np.load(filename)
channel_data = saved_data['channel_data']
t_data = saved_data['t_data']

# plot graphs
for count, y_data in enumerate(channel_data):
    plt.subplot(2, 2, count + 1)
    plt.plot(t_data, y_data)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Time (s)')
    plt.grid(True)

plt.show()
