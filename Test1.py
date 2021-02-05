# Test1 - By: Henry - Wed Jan 22 2020

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 1000)

while(True):
    img=sensor.snapshot()
    img.save('images/' quality=90)
    time.sleep(15)

