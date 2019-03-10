# Motion Detection Camera Software
This software integrates motion detection with the built in webcam utilizing OpenCV 4.0 for Python. So far, the software has been tested on the HP Spectre x360 running Windows 10 and the Raspberry Pi Camera Module on the Raspberry Pi 3 running Raspbian Stretch.

# Requirements
- Python 3.0 or higher
- Python Libraries:
  - OpenCV 4.0
    - installation for Windows: `pip install opencv-contrib-python`
    - [installation for Raspbian Stretch](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/)
    - recommended installation: scipy
  - imutils
  - numpy

# Usage
## Starting the Program
```
usage: mcamera.py [-h] [-p] [-a ANGLE] [-r RESOLUTION RESOLUTION]

Motion detecting software using built-in webcam. Can record motion in both
text and video format.

optional arguments:
  -h, --help            show this help message and exit
  -p                    Enable this option if using the Pi camera module on a
                        Raspberry Pi (default: False)
  -a ANGLE              angle to rotate the video feed in degrees (default: 0
                        degrees)
  -r RESOLUTION RESOLUTION
                        set the resolution of the video feed (default:
                        640x480)
```
## While Running
If started successfully a window like the one below will appear displaying a live feed from the webcame or Pi Camera Module

![Start Image](/images/uponStart.PNG)

### Key Presses
- <d>: Debugging mode that shows the foreground mask in a separate window and bounding boxes around objects in the scene that are considered to be moving 

![Debugging Mode](/images/debug.PNG) 

![Debug Mask](/images/debugMask.PNG)

- <r>: Records and saves frames of the video feed where motion is detected. Frames where no motion is detected are not written to the out file. ***NOTE*** If debugging is enabled while recording, bounding boxes are included in the video file written to the disk
![Recording Mode](/images/recording.PNG)

- <t>: Records the time, date and duration of detected motion and saves it to a text file
