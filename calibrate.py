import numpy as np
import cv2 as cv
import glob

from scipy.spatial.transform import Rotation
from math import cos, sin, radians

# def trig(angle):
#     r = radians(angle)
#     return cos(r), sin(r)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('*.png')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)

#print(objpoints)
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#print(mtx)
cv.destroyAllWindows()

#mtx is a intrinsic matrix
#we have to convert the above intrinsic mtx matrix to 4x4 and have to find the extrinsic matrix
#to find the extrinsic matrix we have to do rotation and then translation
#extrinsic matrix = dot product of rotation and translation matrix
#final camera matrix = dot product of intrinsic and extrinsic matrix

r_obj = Rotation.from_rotvec(np.array(rvecs[0]).reshape(1,3))
rot_matrix = r_obj.as_matrix()

nprvecs = np.array(rvecs)
nptvecs = np.array(tvecs)

## Formation of rotation matrix from rotation vector
# calucation of cos and sin of angle from rotation vector
# since it gives radians we are converting them to degrees
xc, xs = cos(radians(nprvecs[0][0][0])), sin(radians(nprvecs[0][0][0]))
yc, ys = cos(radians(nprvecs[0][1][0])), sin(radians(nprvecs[0][1][0]))
zc, zs = cos(radians(nprvecs[0][2][0])), sin(radians(nprvecs[0][2][0]))

# formation of translation matrix
tx = nptvecs[0][0][0]
ty = nptvecs[0][1][0]
tz = nptvecs[0][2][0]
translation_mtx = np.array([
    [1,0,0,tx],
    [0,1,0,ty],
    [0,0,1,tz],
    [0,0,0,1]
])

#Forming rotation matrix around x, y z axis
rotation_x_matx = np.array([
    [1,0,0,0],
    [0,xc,-xs,0],
    [0,xs,-xc,0],
    [0,0,0,1]
])

rotation_y_matx = np.array([
    [yc,0,ys,0],
    [0,1,0,0],
    [-ys,0,yc,0],
    [0,0,0,1]
])

rotation_z_matx = np.array([
    [zc,-zs,0,0],
    [zs,zc,0,0],
    [0,0,1,0],
    [0,0,0,1]
])

extrensic_matx = np.dot(rotation_z_matx, np.dot(rotation_y_matx, np.dot(rotation_x_matx, translation_mtx)))

#Converting intrinsic matrix from 3X3 to 4X4
intrinsic_matx = np.append( np.append(mtx, [[0],[0],[1]], axis=1), [np.array([0,0,0,1])], axis=0)

#print(mtx)

#Final camera matrix
camera_matrix = np.dot(intrinsic_matx, extrensic_matx)

print('Intrinsinc matrix: ', intrinsic_matx)

print('Extrinsinc matrix, ', extrensic_matx)

print("Final matrix: ", camera_matrix)


cv.destroyAllWindows()