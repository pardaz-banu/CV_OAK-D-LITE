import numpy as np
import cv2 as cv

from scipy.spatial.transform import Rotation
from math import cos, sin, radians

import calibrate


rvecs = calibrate.rvecs
tvecs = calibrate.tvecs

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
intrinsic_matx = np.append( np.append(calibrate.mtx, [[0],[0],[1]], axis=1), [np.array([0,0,0,1])], axis=0)

print(calibrate.mtx)

#Final camera matrix
camera_matrix = np.dot(intrinsic_matx, extrensic_matx)

print('Intrinsinc matrix: ', intrinsic_matx)

print('Extrinsinc matrix, ', extrensic_matx)

print("Final matrix: ", camera_matrix)


cv.destroyAllWindows()


inverse_mat = np.linalg.inv(camera_matrix)

#the dimensions of the image is x = 2, y = 20, z = 15 
projection_points = np.array([[0],[18.5],[32],[1]])

real_world_dim = inverse_mat.dot(projection_points)

print(real_world_dim)

print("length along x axis is : ", real_world_dim[0][0])
print("length along y axis is :", real_world_dim[1][0])
print("length along z axis is :", real_world_dim[2][0])
