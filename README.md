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
### Starting the Program
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
### While Running
If started successfully a window like the one below will appear displaying a live feed from the webcame or Pi Camera Module

![Start Image](/images/uponStart.PNG)

#### Key Presses
- <kbd>D</kbd>: Debugging mode that shows the foreground mask in a separate window and bounding boxes around objects in the scene that are considered to be moving 

![Debugging Mode](/images/debug.PNG) 

![Debug Mask](/images/debugMask.PNG)

- <kbd>R</kbd>: Records and saves frames of the video feed where motion is detected. Frames where no motion is detected are not written to the out file. ***NOTE*** If debugging is enabled while recording, bounding boxes are included in the video file written to the disk

![Recording Mode](/images/recording.PNG)

- <kbd>T</kbd>: Records the time, date and duration of detected motion and saves it to a text file

![Time Stamp Mode](/images/timeStamp.PNG)

  - Example text file output:
```
03-06-2019 21:17:55, 12.1759668140
03-06-2019 21:18:23, 20.7341338090
03-06-2019 21:18:44, 0.1353031140
03-06-2019 21:18:44, 3.0324101540
03-06-2019 21:19:03, 2.5508180800
03-06-2019 21:19:15, 8.5434325880
03-06-2019 21:19:41, 8.9811465130
03-06-2019 21:20:13, 7.1042960370
03-06-2019 21:20:28, 13.4253821270
03-06-2019 21:20:45, 0.1480323770
03-06-2019 21:21:08, 6.7135494260
```
- <kbd>Q</kbd>: Quits the program

#Author
Jack Myers


