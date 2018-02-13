#!/usr/bin/env python2
# -*- coding: utf-8 -*-
u"""Classes to support oscilloscope over GPIB.

Only supports Yokogawa DL1540 for now

@author: Tuomo Kohtamäki
"""

import numpy as np
import gpib
import time
import struct

# Enable for verbose printing
DEBUG = 1


class DL1540:
    """Class to handle Yokogawa DL1540."""

    def __init__(self, gpib_id_high, gpib_id_low):
        """Initialize the connection to oscilloscope using GPIB."""
        self.scope = gpib.dev(gpib_id_high, gpib_id_low)
        if DEBUG:
            print "DL1540 initialized"
            print(self.query("*IDN?"))

    def write(self, command):
        """Write a command to the GPIB bus."""
        gpib.write(self.scope, command)

    def read(self, numbytes):
        """Read the GPIB bus for a given number of bytes."""
        return gpib.read(self.scope, numbytes)

    def query(self, command, numbytes=100):
        """Run a query to the GPIB bus."""
        self.write(command)
        time.sleep(0.1)
        return self.read(numbytes)

    def stop(self):
        """Stop the measurement."""
        self.write("STOP")

    def channels_enabled(self):
        """Query the enabled channels from the scope."""
        self.write("COMM:HEAD 0")
        channels_enabled = [int(self.query("CHANNEL1:MODE?")),
                            int(self.query("CHANNEL2:MODE?")),
                            int(self.query("CHANNEL3:MODE?")),
                            int(self.query("CHANNEL4:MODE?"))]
        return channels_enabled

    def __handle_binary_response(self, data):
        """Handle the binary response from the scope."""
        # The scope first outputs the number of bytes of the length string
        num_lenbytes = int(data[1])
        # Then the length of the data
        num_databytes = int(data[2:2+num_lenbytes])
        payload = data[2+num_lenbytes:2+num_lenbytes+num_databytes]
        return payload, num_lenbytes, num_databytes

    def screen_capture(self):
        """Get a screen capture from the scope."""
        self.write("IMAGE:FORMAT TIFF")
        self.write('IMAGE:SEND?')
        data = self.read(1000000)
        image_data, num_lenbytes, num_databytes = \
            self.__handle_binary_response(data)
        image_bytearray = bytearray(image_data)
        return image_bytearray

    def read_trace(self, channel):
        """Get the displayed traces from the scope."""
        # Set some parameters
        self.write("COMM:HEAD 0")
        self.write("WAVEFORM:DATASELECT ACQDATA")
        self.write("WAVEFORM:FORMAT WORD;BYTEORDER LSBFIRST")
        samplerate = float(self.query("WAVEFORM:SRATE?"))
        self.write("WAVEFORM:TRACE "+str(channel))

        # Get the parameters of the trace
        vdiv = float(self.query("WAVEFORM:VDIV?"))
        offset = float(self.query("WAVEFORM:OFFSET?"))
        data_length = int(self.query("WAVEFORM:LENGTH?"))

        # Number of blocks to fetch
        data_per_block = 5000
        numblocks = int(data_length/data_per_block) + \
            int(data_length % data_per_block > 0)
        this_ch_data = []
        for i in xrange(0, numblocks):
            # Get the block of data
            startblock = i*data_per_block
            if i == (numblocks-1):
                endblock = int(data_length)
            else:
                endblock = (i+1)*data_per_block-1
            if DEBUG:
                print "Getting data from " + str(startblock) + \
                      ' to ' + str(endblock)
            self.write('WAV:START ' + str(startblock) +
                       ';END '+str(endblock)+';SEND?')
            data = self.read(12000)
            # The scope first outputs the number of bytes of the length string
            trace_data, num_lenbytes, num_databytes = \
                self.__handle_binary_response(data)
            numeric_data = struct.unpack("<"+str(num_databytes/2)+"h",
                                         trace_data)
            numeric_data = list(numeric_data)
            this_ch_data += map(lambda x: float(x)*vdiv/3200+offset,
                                numeric_data)

        t = 1/samplerate*np.arange(0, data_length, 1)
        return this_ch_data, t
