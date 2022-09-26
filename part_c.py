from inspect import iscoroutinefunction
import cv2
import numpy as np
import depthai as dai
from unicodedata import name
from operator import imod
#function to extract fram
def getFrame(q):
    frame = q.get()
    return frame.getCvFrame() #converting the frame to openCV formate and then returning it

#function to select mono camera
def getMono(pipe, isLeft):
    mono = pipe.createMonoCamera()
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono

def getStero(pipe, left, right):
    stereo = pipe.createStereoDepth()
    stereo.setLeftRightCheck(True)
    left.out.link(stereo.left)
    right.out.link(stereo.right)
    return  stereo

pipe = dai.Pipeline()

xLeft = pipe.createXLinkOut()
xLeft.setStreamName("Left")

xRight = pipe.createXLinkOut()
xRight.setStreamName("Right")

monoLeft = getMono(pipe, isLeft=True)
monoRight = getMono(pipe, isLeft=False)
stereo = getStero(pipe, monoLeft, monoRight)
xout_left = pipe.createXLinkOut()
xout_left.setStreamName("leftrectify")
xout_right = pipe.createXLinkOut()
xout_right.setStreamName("rightrectify")
xout_display = pipe.createXLinkOut()
xout_display.setStreamName("Disparity")
stereo.disparity.link(xout_display.input)

stereo.rectifiedLeft.link(xout_left.input)
stereo.rectifiedRight.link(xout_right.input)

with dai.Device(pipe) as device:
    disparity_queue = device.getOutputQueue(name = "Disparity", maxSize = 1)
    
    leftQ = device.getOutputQueue(name = "Left", maxSize = 1)
    rightQ = device.getOutputQueue(name = 'Right', maxSize = 1)
    # Calculate a multiplier for color mapping disparity map
    disparityMultiplier = 255 / stereo.initialConfig.getMaxDisparity()
    cv2.namedWindow("Stereo Pair")
    count = 1
    multiplier = 255/stereo.initialConfig.getMaxDisparity()
    while True:
        leftFrame = getFrame(leftQ)
        rightFrame = getFrame(rightQ)
        disparity = (disparity*multiplier).astype(np.uint8)
        imOut = np.uint8(leftFrame/2 + rightFrame/2)
        imOut = cv2.cvtColor(imOut, cv2.COLOR_GRAY2RGB)

        cv2.imshow("Stereo Pair", imOut)
        cv2.imshow("Disparity", disparity)

        k = cv2.waitKey(1)
        if k%256 ==27:
            #Esc pressed
            print("Escape hit, closing operation")
            break
        elif k%256 == 32:
            #Space pressed
            img_name = f"opencv_picture_{count}.png"
            cv2.imwrite(img_name, imOut)
            print(f"{img_name} saved")
            count += 1

cv2.destroyAllWindows()


