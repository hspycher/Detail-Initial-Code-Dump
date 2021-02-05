# Project ATLAS Beacon Detectoin Platform
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import pyb, sensor, image, time, math, ustruct


# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track pink, lime, and orange.
# At the moment, the thresholds must be set manually.
thresholds = [(0, 1, 0, 1, 0, 1), # pink_thresholds
              (30, 45, -40, -20, 0, 40), # lime_thresholds
              (0, 1, 0, 1, 0, 1)] # orange_thresholds
# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.

uart = pyb.UART(3, 9600, timeout_char=1000)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Initializing onboard LED. For testing purposes only.

red_led = pyb.LED(1)
green_led = pyb.LED(2)
blue_led = pyb.LED(3)

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. Don't set "merge=True" becuase that will merge blobs which we don't want here.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=5000, area_threshold=200):

        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        cx = blob.cxf()
        cy = blob.cyf()
        desiredx = 160
        desiredy = 120
        yaw = 1 # 0: Left ; 1: No move ; 2: Right
        pitch = 1 # 0: Down ; 1: No Move ; 2: Up

        if cx < desiredx:
            yaw = 0
        if cx > desiredx:
            yaw = 2
        if cx < 170 | cx > 150:
            yaw = 1

        if cy < desiredy:
            pitch = 0
        if cy > desiredy:
            pitch = 2
        if cy < 130 | cy > 110:
            pitch = 1

        # no color 0
        # pink 1
        # orange 2
        # lime 3

        if blob.code() == 1:
            red_led.on()
            color = 1;
        else:
            red_led.off()
        if blob.code() == 2:
            green_led.on()
            color = 2;
        else:
            green_led.off()
        if blob.code() == 4:
            blue_led.on()
            color = 3;
        else:
            blue_led.off()

        uart.write("<%d, %d, %d>" color, yaw, pitch)
