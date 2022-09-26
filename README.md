# CV_OAK-D-LITE

We use space button to click on images when we run the script. It changes the angle of image to capture when the image capturing is sucessfull otherwise it asks again to click the image.


PART - A:
this part answer is in the python file "calibrate.py" in which we will calculate calibration matrix and along with it I also wrote code to find the intrinsic and extrensic matrices and using these two matrices I have found the camera matrix. 
              camera matrix = [Intrinsic. Extrensic]
We can get camera matrix by dot product of intrinsic and extrensic matrices.
          Extrensic matrix = [Rotation . inverse translation]
to get extrensic matrix we have to do dot product of rotation and inverse of translation matrices.

PART-B:
the answer for this part is present in "part_b.py" which is to find the real world dimensions. In this we get negative values as camera captures mirror image of the original image. 

PART - C:
when I try to run both mono and stereo simultaneously it is giving error as camera unrecognized. 

Question 4:

I had ran the calibration.py for the dataset images that are there then I got the following results:
Intrinsic matrix as:
[[473.4947196    0.         315.63641884]
 [  0.         477.27062032 249.49569168]
 [  0.           0.           1.        ]]
 
 
