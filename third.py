# import cv2
# import numpy as np
# import math
# import json
# import os
# import shutil
# import glob
# import string
# import argparse
# from collections import deque
# xx = 0
# xy = 0
# xz = 0
# yx = 0
# yy = 0
# yz = 0
# zx = 0
# zy = 0
# zz = 0

# parser = argparse.ArgumentParser()
# parser.add_argument("-b", "--bone", type=str, help="The skeleton bone file.")
# args = parser.parse_args()

# def distance(point1, point2):
#     return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
# def signer(value):
#     if value > 0:
#         return 1
#     elif value == 0:
#         return 0
#     else:
#         return -1
# def calc_angle(point1, point2):
#     if point2[1] > point1[1] and point2[0] > point1[0]:
#         return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
#     if point2[1] <= point1[1] and point2[0] > point1[0]:
#         return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
#     if point2[1] > point1[1] and point2[0] < point1[0]:
#         return (180 - math.atan((point2[1] - point1[1]) / (point1[0] - point2[0])) / 3.14 * 180)
#     if point2[1] <= point1[1] and point2[0] <= point1[0]:
#         return (180 + math.atan((point1[1] - point2[1]) / (point1[0] - point2[0])) / 3.14 * 180)
# def calc_json_values(part, angle):
#     if part == "Root":
#         with open(args.bone) as file:
#             data = json.load(file)
#         for item in data:
#             if item['name'] == 'Root':
#                 transform_mat = item['transform_mat']
#                 transform_mat[3][2] = angle
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "RightShoulder":
#         with open(args.bone) as file:
#             data = json.load(file)
#         x = -0.075
#         y = 0.067
#         z = math.cos((angle+90)/2/180*3.14)
#         w = math.sqrt(math.fabs(1-x*x-y*y-z*z))
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'RightShoulder':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)

#     if part == "LeftShoulder":
#         with open(args.bone) as file:
#             data = json.load(file)
#         x = -0.075
#         y = -0.068
#         z = math.cos((angle+90)/2/180*3.14)
#         w = math.sqrt(math.fabs(1-x*x-y*y-z*z))
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'LeftShoulder':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "RightArm":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialRHip = [[0.067, 0.011, -0.997, 0.001], [0.066, 0.011, -0.974, 0.214], [0.059, 0.01, -0.871, 0.487],
#                     [0.046, 0.007, -0.699, 0.714], [0.033, 0.005, -0.493, 0.869], [0.016, 0.002, -0.235, 0.972],
#                     [0, 0, 0, 1], [-0.014, -0.002, 0.215, 0.976], [-0.031, -0.005, 0.467, 0.883], [-0.048, -0.008, 0.711, 0.701], [-0.056, -0.009, 0.839, 0.539], [-0.064, -0.011, 0.961, 0.268], [-0.067, -0.011, 0.997, 0.012]
#                     ]
#         if angle <= -180:
#             angle = -179
#         if angle >= 180:
#             angle = 179
#         angle = angle + 180
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
#         y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
#         z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
#         w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'RightArm':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "RightLeg":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialRHip = [[0.006, -0.031, 0.999, 0.007], [0.021, -0.027, 0.965, 0.259],  [0.036, -0.023, 0.863, 0.502],  [0.048, -0.016, 0.696, 0.715], [0.057, -0.008, 0.49, 0.869], [0.061, 0, 0.239, 0.968], [0.062, 0.008, -0.013, 0.997], [0.058, 0.015, -0.259, 0.964], [0.05, 0.022, -0.522, 0.851],[0.039, 0.027, -0.72, 0.693], [0.027, 0.029, -0.858, 0.513], [0.01, 0.032, -0.968, 0.247], [-0.005, 0.031, -0.999, 0.006]
#                     ]
#         if angle <= -180:
#             angle = -179
#         if angle >= 180:
#             angle = 179
#         angle = angle + 180
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
#         y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
#         z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
#         w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'RightLeg':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "LeftArm":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialRHip = [[-0.084, 0.025, -0.996, 0.004], [-0.081, 0.024, -0.966, 0.244], [-0.073, 0.022, -0.871, 0.485], [-0.06, 0.017, -0.707, 0.704], [-0.043, 0.012, -0.508, 0.86], [-0.021, 0.006, -0.243, 0.97], [0, 0, 0, 1], [0.019, -0.006, 0.228, 0.973], [0.04, -0.012, 0.472, 0.88], [0.059, -0.017,  0.703, 0.708], [0.073, -0.022, 0.867, 0.49], [0.081, -0.024, 0.971, 0.22], [0.084, -0.025, 0.996, 0.05]
#                     ]
#         if angle <= -180:
#             angle = -179
#         if angle >= 180:
#             angle = 179
#         angle = angle + 180
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
#         y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
#         z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
#         w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'LeftArm':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "LeftLeg":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialRHip = [[0.045, -0.117, 0.992, 0.009], [0.038, -0.128, 0.965, 0.224], [ 0.026, -0.134, 0.862, 0.487], [0.013, -0.129, 0.709, 0.692], [-0.002, -0.115, 0.488, 0.865], [-0.016, -0.092, 0.241, 0.965], [-0.028, -0.064, -0.015, 0.997], [-0.04, -0.031, -0.281, 0.958], [-0.048, 0.003, -0.513, 0.857], [-0.053, 0.036, -0.707, 0.704], [-0.053, 0.07, -0.864, 0.495], [-0.051, 0.095, -0.955, 0.275], [-0.047, 0.114, -0.991, 0.044]
#                     ]
#         if angle <= -180:
#             angle = -179
#         if angle >= 180:
#             angle = 179
#         angle = angle + 180
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
#         y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
#         z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
#         w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'LeftLeg':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "RHipJoint":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialRHip = [[0.569, -0.023, 0.778, -0.144], [0.586, -0.358, 0.724, 0.058], [0.568, -0.468, 0.628, 0.251],
#                     [0.507, -0.558, 0.476, 0.454], [0.417, -0.606, 0.304, 0.605], [0.292, -0.613, 0.1, 0.726],
#                     [0.144, -0.576, -0.0115, 0.796]
#                     ]
#         if angle <= -90:
#             angle = -89
#         if angle >= 90:
#             angle = 89
#         angle = angle + 90
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
#         y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
#         z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
#         w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'RHipJoint':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
#     if part == "LHipJoint":
#         with open(args.bone) as file:
#             data = json.load(file)
#         initialLHip = [[0.15, 0.578, 0.1, 0.794], [0.29, 0.614, -0.09, 0.718], [0.43, 0.602, -0.33, 0.582],
#                     [0.509, 0.556, -0.482, 0.446], [0.568, 0.468, -0.629, 0.253], [0.586, 0.034, -0.738, 0.023],
#                     [0.564, 0.203, -0.782, -0.168]
#                     ]
#         if angle <= 90:
#             angle = 91
#         if angle >= 270:
#             angle = 269
#         angle = angle - 90
#         club = int(angle / 30)
#         spare = int(angle % 30)
#         x = initialLHip[club][0] + (initialLHip[club+1][0] - initialLHip[club][0]) / 30 * spare
#         y = initialLHip[club][1] + (initialLHip[club+1][1] - initialLHip[club][1]) / 30 * spare
#         z = initialLHip[club][2] + (initialLHip[club+1][2] - initialLHip[club][2]) / 30 * spare
#         w = initialLHip[club][3] + (initialLHip[club+1][3] - initialLHip[club][3]) / 30 * spare
#         xx = 1-2*(y*y+z*z)
#         xy = 2*(x*y - z*w)
#         xz = 2*(x*z+y*w)
#         yx = 2*(x*y+z*w)
#         yy = 1-2*(x*x+z*z)
#         yz = 2*(y*z-x*w)
#         zx = 2*(x*z-y*w)
#         zy = 2*(y*z+x*w)
#         zz = 1-2*(x*x+y*y)
#         for item in data:
#             if item['name'] == 'LHipJoint':
#                 transform_mat = item['transform_mat']
#                 transform_mat[0][0] = xx
#                 transform_mat[0][1] = xy
#                 transform_mat[0][2] = xz
#                 transform_mat[1][0] = yx
#                 transform_mat[1][1] = yy
#                 transform_mat[1][2] = yz
#                 transform_mat[2][0] = zx
#                 transform_mat[2][1] = zy
#                 transform_mat[2][2] = zz
#         with open(args.bone, 'w') as file:
#             json.dump(data, file)
# def find_corners(image_path):
#     # Read the image
#     main_image = cv2.imread(image_path)
#     height, width, _ = main_image.shape
#     image = main_image[10:height, 10:width]
    
#     directions = [(-1,1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]

#     red_points = np.where((image == [0, 0, 255]).all(axis = -1))  # Array of red points
#     image[red_points] = [255, 255, 255]

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Find corners using the Shi-Tomasi corner detection algorithm
#     corners = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.2, minDistance=0)

#     # Draw circles at the corner locations on the original image
#     body_points = []
#     other_points = []
#     joint_points = []
#     merged_corners = []
#     endpoints = []
    
#     #find the endpoints first
#     # Array of black points
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     for i in range(gray.shape[0]):
#         for j in range(gray.shape[1]):

#             if gray[i][j] == 0:
#                 endpoints.append((i, j))
#     def rotate_point(point, center, alpha):
#     # Convert the angle from degrees to radians
#         alpha_rad = math.radians(alpha)
        
#         # Translate the point relative to the center
#         translated_point = (point[0] - center[0], point[1] - center[1])
        
#         # Apply the rotation transformation
#         rotated_x = translated_point[0] * math.cos(alpha_rad) - translated_point[1] * math.sin(alpha_rad)
#         rotated_y = translated_point[0] * math.sin(alpha_rad) + translated_point[1] * math.cos(alpha_rad)
        
#         # Translate the rotated point back to the original coordinate system
#         final_point = (int(rotated_x + center[0]), int(center[1] - rotated_y))
        
#         return final_point
    
#     for endpoint in endpoints:
#         cv2.circle(image, rotate_point(endpoint, (int(image.shape[0] // 2), int(image.shape[1] // 2)), 17), 1, (0, 0, 0), -1)
        
#     cv2.imwrite("here.png", image)
#     cv2.waitKey(0)

# #         find_corners(image_path)
# find_corners("./2.png")
import math
point1 = (100, 100)
point2 = (70, 100)
   
print(180 + math.atan((point1[1] - point2[1]) / (point1[0] - point2[0])) / 3.14 * 180)

