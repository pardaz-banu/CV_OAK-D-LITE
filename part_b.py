import numpy as np
import cv2

import calibrate

camera_matrix = calibrate.camera_matrix

inverse_mat = np.linalg.inv(camera_matrix)

#the dimensions of the image is x = 2, y = 20, z = 15 
projection_points = np.array([[0],[18.5],[32],[1]])

real_world_dim = inverse_mat.dot(projection_points)

print(real_world_dim)

print("length along x axis is : ", real_world_dim[0][0])
print("length along y axis is :", real_world_dim[1][0])
print("length along z axis is :", real_world_dim[2][0])