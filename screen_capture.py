import datetime
from scope_functions import DL1540

filename = 'captures/'+datetime.datetime.now().isoformat()+'.tiff'

scope=DL1540(0,1)
scope.stop()

image_bytearray = scope.screen_capture()
newFile = open(filename, "wb")
newFile.write(image_bytearray)
