#!/usr/bin/env python2
# -*- coding: utf-8 -*-
u"""Capture the displayed traces from the oscilloscope.

The data is saved to traces/ folder. It can be displayed by running the
plot_saved_data.py script.

@author: Tuomo Kohtamäki
"""
import numpy as np
import datetime
from scope_functions import DL1540

filename = 'traces/'+datetime.datetime.now().isoformat()+'.npz'

scope = DL1540(0, 1)
scope.stop()

channels_enabled = scope.channels_enabled()

channel_data = list([])

for ch_idx, enabled in enumerate(channels_enabled):
    if enabled:
        this_ch_data, t_data = scope.read_trace(ch_idx+1)
        channel_data.append(np.array(this_ch_data))

channel_data = np.array(channel_data)

np.savez_compressed(filename, channel_data=channel_data, t_data=t_data)

# Plotting moved to plot_saved_data.py
