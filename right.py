import cv2
import numpy as np
import math
import json
import os
import shutil
import glob
import string
import argparse
from collections import deque
xx = 0
xy = 0
xz = 0
yx = 0
yy = 0
yz = 0
zx = 0
zy = 0
zz = 0

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bone", type=str, help="The skeleton bone file.")
args = parser.parse_args()

def distance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
def signer(value):
    if value > 0:
        return 1
    elif value == 0:
        return 0
    else:
        return -1
def calc_angle(point1, point2):
    if point2[1] > point1[1] and point2[0] > point1[0]:
        return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
    if point2[1] <= point1[1] and point2[0] > point1[0]:
        return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
    if point2[1] > point1[1] and point2[0] < point1[0]:
        return (180 - math.atan((point2[1] - point1[1]) / (point1[0] - point2[0])) / 3.14 * 180)
    if point2[1] <= point1[1] and point2[0] <= point1[0]:
        if point2[0] == point1[0]:
            return 270
        return (180 + math.atan((point1[1] - point2[1]) / (point1[0] - point2[0])) / 3.14 * 180)
def calc_json_values(part, angle):
    if part == "Root":
        with open(args.bone) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][0] = angle
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "Root1":
        with open(args.bone) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][1] = angle
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "Root2":
        with open(args.bone) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][2] = angle
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "RightShoulder":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[0.483, -0.516, -0.44, 0.554], [0.616, -0.376, -0.564, 0.401], [0.693, -0.234, -0.635, 0.247], [0.733, -0.065, -0.674, 0.063], [0.721, 0.13, -0.664, -0.148], [0.656, 0.302, -0.606, -0.334], [0.555, 0.441, -0.514, -0.483], [0.416, 0.557, -0.386, -0.606], [0.246, 0.638, -0.23, -0.692], [0.05, 0.677, -0.05, -0.733], [-0.141, 0.667, 0.125, -0.721], [-0.303, 0.621, 0.274, -0.669], [-0.478, 0.52, 0.435, -0.558]]
        if angle <= -180:
            angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'RightShoulder':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "LeftShoulder":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[-0.456, 0.537, 0.494, -0.509],[-0.57, 0.395, 0.612, -0.38],[-0.643, 0.242, 0.687, -0.238],[-0.683, 0.052, 0.726, -0.061],[-0.677, -0.127, 0.717, 0.108],[-0.621, -0.321, 0.654, 0.289],[-0.517, -0.488, 0.542, 0.448],[-0.374, -0.619, 0.387, 0.572],[-0.24, -0.689, 0.243, 0.64],[-0.057, -0.729, 0.048, 0.68],[0.137, -0.713, -0.158, 0.669],[0.286, -0.659, -0.315, 0.62],[0.441, -0.552, -0.478, 0.522]]
        if angle <= -180:
            angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'LeftShoulder':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "RightArm":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[ 0.083, -0.008, -0.996, 0.005], [0.081, -0.008, -0.966, 0.243], [0.073, -0.007, -0.874, 0.481], [ 0.059, -0.006, -0.71, 0.71], [0.041, -0.004, -0.491, 0.87], [0.021, -0.002, -0.257, 0.966], [0, 0, 0, 1], [-0.022, 0.002, 0.27, 0.962], [-0.04, 0.004, 0.478, 0.877], [-0.059, 0.006, 0.71, 0.7], [-0.073, 0.007, 0.878, 0.471], [-0.08, 0.008, 0.976, 0.201], [-0.083, 0.008, 0.996, -0.006]
                    ]
        if angle <= -180:
            angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'RightArm':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "RightLeg":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[0.006, -0.031, 0.999, 0.007], [0.021, -0.027, 0.965, 0.259],  [0.036, -0.023, 0.863, 0.502],  [0.048, -0.016, 0.696, 0.715], [0.057, -0.008, 0.49, 0.869], [0.061, 0, 0.239, 0.968], [0.062, 0.008, -0.013, 0.997], [0.058, 0.015, -0.259, 0.964], [0.05, 0.022, -0.522, 0.851],[0.039, 0.027, -0.72, 0.693], [0.027, 0.029, -0.858, 0.513], [0.01, 0.032, -0.968, 0.247], [-0.005, 0.031, -0.999, 0.006]
                    ]
        if angle <= -180:
            angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'RightLeg':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "LeftArm":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[-0.063, 0.016, -0.997, -0.004], [-0.06, 0.015, -0.962, 0.265], [-0.055, 0.014, -0.874, 0.481], [-0.045, 0.011, -0.713, 0.7], [-0.032, 0.008, -0.505, 0.862], [-0.016, 0.004, -0.258, 0.966], [-0.001, 0.000, -0.017, 0.999], [0.016, -0.004, 0.251, 0.967], [0.031, -0.007, 0.483, 0.874], [0.044, -0.011, 0.703, 0.709], [0.055, -0.013, 0.864, 0.5], [0.06, -0.015, 0.956, 0.284], [0.063, -0.016, 0.997,0.009]
                    ]
        if angle <= -180:
            angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'LeftArm':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "LeftLeg":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[0.045, -0.117, 0.992, 0.009], [0.038, -0.128, 0.965, 0.224], [ 0.026, -0.134, 0.862, 0.487], [0.013, -0.129, 0.709, 0.692], [-0.002, -0.115, 0.488, 0.865], [-0.016, -0.092, 0.241, 0.965], [-0.028, -0.064, -0.015, 0.997], [-0.04, -0.031, -0.281, 0.958], [-0.048, 0.003, -0.513, 0.857], [-0.053, 0.036, -0.707, 0.704], [-0.053, 0.07, -0.864, 0.495], [-0.051, 0.095, -0.955, 0.275], [-0.047, 0.114, -0.991, 0.044]
                    ]
        if angle <= -180:
         angle = -179
        if angle >= 180:
            angle = 179
        angle = angle + 180
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'LeftLeg':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "RHipJoint":
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[0.516, -0.554, 0.487, 0.436], [0.422, -0.607, 0.308, 0.598], [0.321, -0.618, 0.141, 0.703], [0.162, -0.586, -0.092, 0.789], [-0.012, -0.501, -0.317, 0.805], [-0.166, -0.389, -0.494, 0.76], [-0.295, -0.266, -0.624, 0.674], [-0.403, -0.131, -0.716, 0.555], [-0.512, 0.055, -0.779, 0.356], [-0.571, 0.215, -0.777, 0.153], [-0.59, 0.351, -0.725, -0.046], [-0.572, 0.465, -0.63, -0.243], [-0.521, 0.55, -0.496, -0.425]]
        # if angle <= -90:
        #     angle = -89
        # if angle >= 90:
        #     angle = 89
        if angle <= 0:
            angle += 360

        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'RHipJoint':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
    if part == "LHipJoint":
        with open(args.bone) as file:
            data = json.load(file)
        initialLHip = [[-0.301, 0.251, 0.637, 0.663], [-0.187, 0.365, 0.523, 0.747], [-0.053, 0.469, 0.371, 0.798], [0.15, 0.578, 0.1, 0.794], [0.29, 0.614, -0.09, 0.718], [0.43, 0.602, -0.33, 0.582],
                    [0.509, 0.556, -0.482, 0.446], [0.568, 0.468, -0.629, 0.253], [0.586, 0.034, -0.738, 0.071],
                    [0.564, 0.203, -0.782, -0.168], [0.518, -0.074, -0.786, -0.33], [0.438, -0.079, -0.744, -0.502], [0.312, 0.238, -0.647, -0.653]
                    ]
        # if angle <= 90:
        #     angle = 91
        # if angle >= 270:
        #     angle = 269
        # angle = angle - 90
        if angle <= 0:
            angle += 360
        club = int(angle / 30)
        spare = int(angle % 30)
        x = initialLHip[club][0] + (initialLHip[club+1][0] - initialLHip[club][0]) / 30 * spare
        y = initialLHip[club][1] + (initialLHip[club+1][1] - initialLHip[club][1]) / 30 * spare
        z = initialLHip[club][2] + (initialLHip[club+1][2] - initialLHip[club][2]) / 30 * spare
        w = initialLHip[club][3] + (initialLHip[club+1][3] - initialLHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'LHipJoint':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)

def find_corners(image_path):
    # Read the image
    main_image = cv2.imread(image_path)
    height, width, _ = main_image.shape
    image = main_image[130:height, 10:width]
    height1, width1, _ = image.shape

  

    directions = [(-1,1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find corners using the Shi-Tomasi corner detection algorithm
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.2, minDistance=0)

    # Draw circles at the corner locations on the original image
    body_points = []
    other_points = []
    joint_points = []
    merged_corners = []
    endpoints = []
    
    #find the endpoints first
    black_points = np.argwhere(gray == 0)  # Array of black points
    min_y = np.min(black_points[:, 1])
    max_y = np.max(black_points[:, 1])
    heihtance = max_y - min_y
    #find the high length
    x_position = math.log2(450 / heihtance)
    
    endpoints = []
    array1 = np.array([(-1, -1), (-1, 0)])
    array2 = np.array([(-1, 0), (-1, 1)])
    array3 = np.array([(-1, 1), (0, 1)])
    array4 = np.array([(0, 1), (1, 1)])
    array5 = np.array([(1, 1), (1, 0)])
    array6 = np.array([(1, 0), (1, -1)])
    array7 = np.array([(1, -1), (0, -1)])
    array8 = np.array([(-1, -1), (0, -1)])
    for point in black_points:
        py, px = point
        connections = 0
        direction_array = np.array([])
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            nx, ny = px + dx, py + dy
            for iter_point in black_points:
                if iter_point[0] == ny and iter_point[1] == nx:
                    connections += 1
                    direction_array = np.append(direction_array, np.array([dx, dy]))
        direction_array = direction_array.reshape(-1, 2)
        if connections == 1:
            endpoints.append((px, py))
        if connections == 2:
            result1 = np.array_equal(array1, direction_array)
            result2 = np.array_equal(array2, direction_array)
            result3 = np.array_equal(array3, direction_array)
            result4 = np.array_equal(array4, direction_array)
            result5 = np.array_equal(array5, direction_array)
            result6 = np.array_equal(array6, direction_array)
            result7 = np.array_equal(array7, direction_array)
            result8 = np.array_equal(array8, direction_array)
            result = any([result1, result2, result3, result4, result5, result6, result7, result8])
            if result == True:
                con = 0

                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                    nx, ny = px + dx, py + dy
                    for iter_point in black_points:
                        if iter_point[0] == ny and iter_point[1] == nx:
                            for dx1, dy1 in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                                nx1, ny1 = ny + dx1, nx + dy1
                                for ipoint in black_points:
                                    if ipoint[0] == ny1 and ipoint[1] == nx1:
                                        con += 1
                if con < 6:
                    endpoints.append((px, py))
    

    if corners is not None:
        corners = np.intp(corners)
        for corner in corners:
            x, y = corner.ravel()
            merge = True
            for cx, cy in merged_corners:
                if np.sqrt((x - cx)**2 + (y - cy)**2) < 10:
                    merge = False
                    break
            if merge:
                merged_corners.append((x, y))
            
        for corner_point in merged_corners:
            x, y = corner_point[0], corner_point[1]
            nearby_points = []
            for dx in range(-8, 8):
                for dy in range(-8, 8):
                    if dx**2 + dy**2 >= 36:
                        nx, ny = x + dx, y + dy
                        if ny >= 0 and ny < gray.shape[0] and nx >= 0 and nx < gray.shape[1]:
                            nearby_points.append((nx, ny))
                            
            # Find the black dots from the nearby points
            black_dots = []
            for point in nearby_points:
                px, py = point
                if gray[py, px] == 0:
                    black_dots.append(point)
            # Find the direction factors from the black dots to the (x, y) point
            max_distance = 10
            for i, point1 in enumerate(black_dots):
                # Skip the first point
                if i == 0:
                    continue

                # Iterate over the remaining points
                for point2 in black_dots[i:]:
                    # Calculate the distance between the two points
                    distance1 = distance(point1, point2)

                    # If the distance is less than the threshold, merge the points
                    if distance1 < max_distance:

                        if point2 in black_dots:

                            black_dots.remove(point2)

            if len(black_dots) != 2:
                if len(black_dots) > 2:
                    body_points.append((x, y))
                    # cv2.circle(image, (x, y), 3, (255, 0, 0), -1)
                else:
                    other_points.append((x, y))
                    # cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            else:
                joint_points.append((x, y))
                # cv2.circle(image, (x, y), 3, (0, 0, 255), -1)


    if len(body_points) >= 2:
        if body_points[0][1] < body_points[1][1]:
            upperpoint = body_points[0]
            lowerpoint = body_points[1]
        else: 
            upperpoint = body_points[1]
            lowerpoint = body_points[0]
    else:
        upperpoint = (int(gray.shape[1] / 2), int(gray.shape[0] / 3))
        lowerpoint = (int(gray.shape[1] / 2), int(gray.shape[0] / 3 * 2))

    endpoints = [endpoint for endpoint in endpoints if not (distance(endpoint, upperpoint) <= 40 or distance(endpoint, lowerpoint) <= 40)]
    
    joint_points = [joint_point for joint_point in joint_points if not (distance(joint_point, upperpoint) <= 40 or distance(joint_point, lowerpoint) <= 40)]
    for joint_point in joint_points:
        endpoints = [endpoint for endpoint in endpoints if not (distance(endpoint, joint_point) <= 40)]
    
    if len(endpoints) <= 4:
        return
    while len(endpoints) > 5:
        del endpoints[-1]
    
    if len(other_points) != 5:
        if len(endpoints) == 5:
            other_points.clear()
            other_points = endpoints
    
    expanded_upper_points = []
    expanded_lower_points = []
    x, y = upperpoint
    for i in range(-7, 8):
        for j in range(-7, 8):
            expanded_upper_points.append((x + i, y + j))
    x, y = lowerpoint
    for i in range(-7, 8):
        for j in range(-7, 8):
            expanded_lower_points.append((x + i, y + j))
    part_points_array = []
    expand_part_points_array = []
    is_arm = []
    is_leg = []
    index = 0

    def find_parts(start_point):
        x, y = start_point
        real_start_points = []

        for dx in range(-3, 3):
            for dy in range(-3, 3):
                nx, ny = dx + x, dy + y
                if gray[ny, nx] == 0:
                    real_start_points.append((nx, ny))
        x, y = real_start_points[0]

        queue = deque()
        visited = set()
        arm = 0
        leg = 0
        queue.append((x,y))
        for dx, dy in directions:
            next_x = x + dx
            next_y = y + dy
            if gray[next_y, next_x] == 0:  # Check if the pixel is black
                x, y = next_x, next_y
                if (x, y) in queue:
                    continue
                else:
                    queue.append((x,y))
        while queue:
            current_point = queue.popleft()
            x, y = current_point
            visited.add((x, y))

            if (x, y) in expanded_lower_points:
                leg = 1
                break
            if (x, y) in expanded_upper_points:
                arm = 1
                break

            for dx, dy in directions:
                next_x = x + dx
                next_y = y + dy

                if (next_x, next_y) not in visited:
                    if next_x >= 0 and next_x < image.shape[1] and next_y >= 0 and next_y < image.shape[0]:
                        if gray[next_y, next_x] == 0:  # Check if the pixel is black
                            if (next_x, next_y) in queue:
                                continue
                            else:
                                queue.append((next_x, next_y))
            if not queue:
                for dx in range(-5, 6):
                    for dy in range(-5, 6):
                        next_x = x + dx
                        next_y = y + dy
                        if (next_x, next_y) not in visited:
                            if next_x >= 0 and next_x < image.shape[1] and next_y >= 0 and next_y < image.shape[0]:
                                if gray[next_y, next_x] == 0:  # Check if the pixel is black
                                    queue.append((next_x, next_y))
        # for black_line_point in visited:
        #     cv2.circle(image, black_line_point, 2, (122, 122, 0), -1)
        return visited, arm, leg

    for other_point in other_points:
        part_points, arm, leg = find_parts(other_point)
        part_points_array.append(part_points)
        is_arm.append(arm)
        is_leg.append(leg)
        index += 1

    for points in part_points_array:
        expand_points = set()
        for point in points:
            x, y = point
            for i in range(-4, 5):
                for j in range(-4, 5):
                    expand_points.add((x + i, y + j))
        expand_part_points_array.append(expand_points)

   
    arms = []
    arms_num = []
    legs = []
    legs_num = []
    index = 0
    for expand_points in expand_part_points_array:
        if is_arm[index] == 0:
            legs.append(next((point for point in other_points if point in expand_points), None))
            legs_num.append(index)
        if is_arm[index] == 1:
            arms.append(next((point for point in other_points if point in expand_points), None))
            arms_num.append(index)
        index += 1
    if len(arms) < 2 or len(legs) < 2:
        return
    # for point in legs:
    #     cv2.circle(image, point, 7, (122, 122, 0), -1)
    # for point in arms:
    #     cv2.circle(image, point, 7, (122, 0, 122), -1)
    final = []
    if len(legs) == 3:
        final = legs
    if len(arms) == 3:
        final = arms

    def distance_to_line(point, line_start, line_end):
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end

        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        return numerator / denominator

    # Calculate the distance of each point in the final array from the line
    distances = []

    for point in final:
        distance_line = distance_to_line(point, upperpoint, lowerpoint)
        distances.append(distance_line)

    # Find the index of the point with the minimum distance
    closest_point_index = distances.index(min(distances))
    closest_point = final[closest_point_index]
    head_point = closest_point

    for point in other_points:
       if point[0] == head_point[0] and point[1] == head_point[1]:
          other_points.remove(point)
          break
    if distance(head_point, upperpoint) > distance(head_point, lowerpoint):
        temp = lowerpoint
        lowerpoint = upperpoint
        upperpoint = temp

    # cv2.circle(image, head_point, 9, (0, 0, 122), -1)
    # cv2.circle(image, upperpoint, 7, (0, 0, 122), -1)
    # cv2.circle(image, lowerpoint, 5, (0, 0, 122), -1)


    xpanded_upper_points = []
    expanded_lower_points = []
    # print(upperpoint, lowerpoint)
    x, y = upperpoint
    for i in range(-7, 8):
        for j in range(-7, 8):
            expanded_upper_points.append((x + i, y + j))
    x, y = lowerpoint
    for i in range(-7, 8):
        for j in range(-7, 8):
            expanded_lower_points.append((x + i, y + j))
    part_points_array = []
    expand_part_points_array = []
    is_arm = []
    is_leg = []
    for other_point in other_points:
        part_points, arm, leg = find_parts(other_point)
        part_points_array.append(part_points)
        is_arm.append(arm)
        is_leg.append(leg)
        index += 1
        # print("hello")
        # print(index)
    for points in part_points_array:
        expand_points = set()
        for point in points:
            x, y = point
            for i in range(-4, 5):
                for j in range(-4, 5):
                    expand_points.add((x + i, y + j))
        expand_part_points_array.append(expand_points)
    arms = []
    arms_num = []
    legs = []
    legs_num = []
    index = 0
    for expand_points in expand_part_points_array:
        if is_arm[index] == 0:
            legs.append(next((point for point in other_points if point in expand_points), None))
            legs_num.append(index)
        if is_arm[index] == 1:
            arms.append(next((point for point in other_points if point in expand_points), None))
            arms_num.append(index)
        index += 1
    if len(arms) < 2 or len(legs) < 2:
        return

    def point_furthest_to_right(a, b, points):
        max_x_projection = float("-inf")
        furthest_point = None
        
        for point in points:
            # Calculate the x-coordinate projection
            x_projection = ((b[1] - a[1]) * (point[0] - a[0]) + (a[0] - b[0]) * (point[1] - a[1])) / ((b[1] - a[1]) ** 2 + (a[0] - b[0]) ** 2)
            
            if x_projection > max_x_projection:
                max_x_projection = x_projection
                furthest_point = point
        
        return furthest_point

    right_arm = point_furthest_to_right(upperpoint, lowerpoint, arms)
    right_leg = point_furthest_to_right(upperpoint, lowerpoint, legs)
    
    index = 0
    for arm in arms:
        if right_arm[0] == arm[0] and right_arm[1] == arm[1]:
            break
        index += 1
    if index == 0:
        right_arm_num = arms_num[0]
        left_arm = arms[1]
        left_arm_num = arms_num[1]
    else:
        right_arm_num = arms_num[1]
        left_arm_num = arms_num[0]
        left_arm = arms[0]

    index = 0
    for leg in legs:
        if right_leg[0] == leg[0] and right_leg[1] == leg[1]:
            break
        index += 1
    if index == 0:
        right_leg_num = legs_num[0]
        left_leg = legs[1]
        left_leg_num = legs_num[1]
    else:
        right_leg_num = legs_num[1]
        left_leg_num = legs_num[0]
        left_leg = legs[0]

    # cv2.circle(image, left_arm, 8, (0, 0, 255), -1)
    # cv2.circle(image, right_arm, 8, (0, 0, 122), -1)
    # cv2.circle(image, left_leg, 8, (0, 255, 0), -1)
    # cv2.circle(image, right_leg, 8, (0, 122, 0), -1)

    def get_middle(array):
        array_list = list(array)
        middle_index = len(array_list) // 2
        middle_point = array[middle_index]
        return middle_point
    def get_average_point(array):
        sx = 0
        sy = 0
        for point in array:
            x, y = point
            sx += x
            sy += y
        return (sx // len(array), sy // len(array))
    joint_right_arms = [point for point in joint_points if point in expand_part_points_array[right_arm_num]]
    joint_right_legs = [point for point in joint_points if point in expand_part_points_array[right_leg_num]]
    joint_left_arms = [point for point in joint_points if point in expand_part_points_array[left_arm_num]]
    joint_left_legs = [point for point in joint_points if point in expand_part_points_array[left_leg_num]]
    
    if len(joint_left_arms) == 1:
        joint_left_arm = joint_left_arms[0]
    else:
        joint_left_arms.append(get_middle(np.sort(list(part_points_array[left_arm_num]), axis = 0)))
        joint_left_arm = get_average_point(joint_left_arms)
    
    if len(joint_right_arms) == 1:
        joint_right_arm = joint_right_arms[0]
    else:
        joint_right_arms.append(get_middle(np.sort(list(part_points_array[right_arm_num]), axis = 0)))
        joint_right_arm = get_average_point(joint_right_arms)
    
    if len(joint_right_legs) == 1:
        joint_right_leg = joint_right_legs[0]
    else:
        joint_right_legs.append(get_middle(np.sort(list(part_points_array[right_leg_num]), axis = 0)))
        joint_right_leg = get_average_point(joint_right_legs)

    if len(joint_left_legs) == 1:
        joint_left_leg = joint_left_legs[0]
    else:
        joint_left_legs.append(get_middle(np.sort(list(part_points_array[left_leg_num]), axis = 0)))
        joint_left_leg = get_average_point(joint_left_legs)

    # cv2.circle(image, joint_left_arm, 7, (0, 200, 200), -1)
    # cv2.circle(image, joint_right_arm, 7, (0, 200, 200), -1)
    # cv2.circle(image, joint_right_leg, 7, (0, 200, 200), -1)
    # cv2.circle(image, joint_left_leg, 7, (0, 200, 200), -1)

    
    angle_rad = math.atan2(lowerpoint[1] - head_point[1], lowerpoint[0] - head_point[0])
    angle_deg = math.degrees(angle_rad) + 180
    def rotate_point(point, center, alpha):
    # Convert the angle from degrees to radians
        alpha_rad = math.radians(alpha) 
        
        # Translate the point relative to the center
        translated_point = (point[0] - center[0], point[1] - center[1])
        
        # Apply the rotation transformation
        rotated_x = translated_point[0] * math.cos(alpha_rad) - translated_point[1] * math.sin(alpha_rad)
        rotated_y = translated_point[0] * math.sin(alpha_rad) + translated_point[1] * math.cos(alpha_rad)
        
        # Translate the rotated point back to the original coordinate system
        final_point = (int(rotated_x + center[0]), int(center[1] - rotated_y))
        
        return final_point
    left_arm = rotate_point((left_arm[1], left_arm[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    right_arm = rotate_point((right_arm[1], right_arm[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    left_leg =  rotate_point((left_leg[1], left_leg[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    right_leg = rotate_point((right_leg[1], right_leg[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    joint_left_arm = rotate_point((joint_left_arm[1], joint_left_arm[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    joint_right_arm = rotate_point((joint_right_arm[1], joint_right_arm[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    joint_left_leg = rotate_point((joint_left_leg[1], joint_left_leg[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    joint_right_leg = rotate_point((joint_right_leg[1], joint_right_leg[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    upperpoint = rotate_point((upperpoint[1], upperpoint[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)
    lowerpoint = rotate_point((lowerpoint[1], lowerpoint[0]), (int(image.shape[0] // 2), int(image.shape[1] // 2)), angle_deg)

    # cv2.circle(image, (left_arm[0], left_arm[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (right_arm[0], right_arm[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (left_leg[0], left_leg[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (right_leg[0], right_leg[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (joint_left_arm[0], joint_left_arm[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (joint_right_arm[0],joint_right_arm[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (joint_left_leg[0], joint_left_leg[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (joint_right_leg[0], joint_right_leg[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (upperpoint[0], upperpoint[1] -400) , 5, (0, 0, 255), -1)
    # cv2.circle(image, (lowerpoint[0], lowerpoint[1] -400) , 5, (0, 0, 255), -1)

    angle_left_arm = calc_angle(left_arm, joint_left_arm)
    angle_right_arm = calc_angle(right_arm, joint_right_arm)
    angle_left_leg = calc_angle(left_leg, joint_left_leg)
    angle_right_leg = calc_angle(right_leg, joint_right_leg)

    angle_joint_left_arm = calc_angle(joint_left_arm, upperpoint)
    angle_joint_right_arm = calc_angle(joint_right_arm, upperpoint)
    angle_joint_left_leg = calc_angle(joint_left_leg, lowerpoint)
    angle_joint_right_leg = calc_angle(joint_right_leg, lowerpoint)
    
    rightshoulder = 0
    if angle_joint_left_arm <= -180:
        calc_json_values("RightShoulder", angle_joint_left_arm + 360)
        rightshoulder = angle_joint_left_arm + 360
    elif angle_joint_left_arm >= 180:
        calc_json_values("RightShoulder", angle_joint_left_arm - 360)
        rightshoulder =  angle_joint_left_arm - 360
    else:
        calc_json_values("RightShoulder", angle_joint_left_arm)
        rightshoulder = angle_joint_left_arm

    left_shoulder = 0
    if angle_joint_right_arm <= -180:
        calc_json_values("LeftShoulder", angle_joint_right_arm + 360)
        left_shoulder = angle_joint_right_arm + 360
    elif angle_joint_right_arm >= 180:
        calc_json_values("LeftShoulder", angle_joint_right_arm - 360)
        left_shoulder = angle_joint_right_arm - 360
    else:
        calc_json_values("LeftShoulder", angle_joint_right_arm)
        left_shoulder = angle_joint_right_arm

    # if angle_joint_right_arm <= -180:
    #     calc_json_values("RightShoulder", angle_joint_right_arm + 360)
    # elif angle_joint_right_arm >= 180:
    #     calc_json_values("RightShoulder", angle_joint_right_arm - 360)
    # else:
    #     calc_json_values("RightShoulder", angle_joint_right_arm)

    # if angle_joint_left_arm <= -180:
    #     calc_json_values("LeftShoulder", angle_joint_left_arm + 360)
    # elif angle_joint_left_arm >= 180:
    #     calc_json_values("LeftShoulder", angle_joint_left_arm - 360)
    # else:
    #     calc_json_values("LeftShoulder", angle_joint_left_arm)
    
    calc_json_values("RHipJoint", angle_joint_left_leg)
    calc_json_values("LHipJoint", angle_joint_right_leg)

    right_arm1 = 0
    if angle_joint_left_arm - angle_left_arm <= -180:
        calc_json_values("RightArm", angle_joint_left_arm - angle_left_arm + 360)
        right_arm1 = angle_joint_left_arm - angle_left_arm + 360
    elif angle_joint_left_leg - angle_left_arm >= 180:
        calc_json_values("RightArm", angle_joint_left_arm - angle_left_arm - 360)
        right_arm1 = angle_joint_left_arm - angle_left_arm - 360
    else:
        calc_json_values("RightArm", angle_joint_left_arm - angle_left_arm)
        right_arm1 = angle_joint_left_arm - angle_left_arm

    right_leg1 = 0
    if angle_joint_left_leg - angle_left_leg <= -180:
        calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg + 360)
        right_leg1 = angle_joint_left_leg - angle_left_leg + 360
    elif angle_joint_left_leg - angle_left_leg >= 180:
        calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg - 360)
        right_leg1 = angle_joint_left_leg - angle_left_leg - 360
    else:
        calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg)
        right_leg1 = angle_joint_left_leg - angle_left_leg

    left_arm1 = 0
    if angle_joint_right_arm - angle_right_arm >= 180:
        calc_json_values("LeftArm", angle_joint_right_arm - angle_right_arm - 360)
        left_arm1 = angle_joint_right_arm - angle_right_arm - 360
    elif angle_joint_right_arm - angle_right_arm <= -180:
        calc_json_values("LeftArm", angle_joint_right_arm - angle_right_arm + 360)
        left_arm1 = angle_joint_right_arm - angle_right_arm - 360
    else:
        calc_json_values("LeftArm", angle_joint_right_arm - angle_right_arm)
        left_arm1 = angle_joint_right_arm - angle_right_arm

    left_leg1 = 0
    if angle_joint_right_leg - angle_right_leg >= 180:
        calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg - 360)
        left_leg1 = angle_joint_right_leg - angle_right_leg - 360
    elif angle_joint_right_leg - angle_right_leg <= -180:
        calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg + 360)
        left_leg1 = angle_joint_right_leg - angle_right_leg + 360
    else:
        calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg)
        left_leg1 = angle_joint_right_leg - angle_right_leg

    # if angle_joint_left_arm - angle_left_arm <= -180:
    #     calc_json_values("LeftArm", angle_joint_left_arm - angle_left_arm + 360)
    # elif angle_joint_left_leg - angle_left_arm >= 180:
    #     calc_json_values("LeftArm", angle_joint_left_arm - angle_left_arm - 360)
    # else:
    #     calc_json_values("LeftArm", angle_joint_left_arm - angle_left_arm)

    # if angle_joint_left_leg - angle_left_leg <= -180:
    #     calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg + 360)
    # elif angle_joint_left_leg - angle_left_leg >= 180:
    #     calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg - 360)
    # else:
    #     calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg)


    # if angle_joint_right_arm - angle_right_arm >= 180:
    #     calc_json_values("RightArm", angle_joint_right_arm - angle_right_arm - 360)
    # elif angle_joint_right_arm - angle_right_arm <= -180:
    #     calc_json_values("RightArm", angle_joint_right_arm - angle_right_arm + 360)
    # else:
    #     calc_json_values("RightArm", angle_joint_right_arm - angle_right_arm)
    
    # if angle_joint_right_leg - angle_right_leg >= 180:
    #     calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg - 360)
    # elif angle_joint_right_leg - angle_right_leg <= -180:
    #     calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg + 360)
    # else:
    #     calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg)

   

    if left_arm[0]/2 + right_arm[0]/2 > upperpoint[0]:
        rotate_angle = calc_angle(((int(left_arm[0]/2 + right_arm[0]/2)), int((right_arm[1]/2 + left_arm[1]/2))), head_point)
    else:
        rotate_angle = calc_angle(((int(left_arm[0]/2 + right_arm[0]/2)), int((right_arm[1]/2 + left_arm[1]/2))), upperpoint)
    
    def json_rotate(angle, angle_1):
        # print(angle)
        with open(args.bone) as file:
            data = json.load(file)
        if angle >= 180:
            angle -= 180
            
        if  -90 <= angle < 0:
            angle = 0 - angle
        elif angle < -90:
            angle  = 180 + angle
        else:
            angle = angle - 90
        
        y = math.sin(angle/180*3.14) / math.sqrt(2)
        z = y
        value = math.sqrt(math.fabs(0.5 - y * y))
        if angle <= 90:
            x = (-1) * value
            w = value
        if angle > 90:
            x = value
            w = (-1) * value
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)

        with open(args.bone) as file:
            data = json.load(file)
        if angle >= 180:
            angle -= 180
            
        if  -90 <= angle < 0:
            angle = 0 - angle
        elif angle < -90:
            angle  = 180 + angle
        else:
            angle = angle - 90
        
        y = math.sin(angle/180*3.14) / math.sqrt(2)
        z = y
        value = math.sqrt(math.fabs(0.5 - y * y))
        if angle <= 90:
            x = (-1) * value
            w = value
        if angle > 90:
            x = value
            w = (-1) * value
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)
        with open(args.bone) as file:
            data = json.load(file)
        initialRHip = [[-0.707, 0.708, 0.00, 0.00], [-0.688, 0.687, 0.164, 0.164], [-0.614, 0.615, 0.35, 0.35], [-0.509, 0.508, 0.491, 0.491], [-0.365, 0.364, 0.605, 0.605], [-0.178, 0.177, 0.684, 0.684], [-0.013, 0.012, 0.707, 0.707], [0.143, -0.144, 0.692, 0.692], [0.336, -0.337, 0.621, 0.621], [0.482, -0.483, 0.516, 0.516], [0.603, -0.604, 0.368, 0.368], [0.679, -0.68, 0.194, 0.194], [0.707, -0.708, 0.00, 0.00]
                    ]
        club = int(angle_1 / 30)
        spare = int(angle_1 % 30)
        x = initialRHip[club][0] + (initialRHip[club+1][0] - initialRHip[club][0]) / 30 * spare
        y = initialRHip[club][1] + (initialRHip[club+1][1] - initialRHip[club][1]) / 30 * spare
        z = initialRHip[club][2] + (initialRHip[club+1][2] - initialRHip[club][2]) / 30 * spare
        w = initialRHip[club][3] + (initialRHip[club+1][3] - initialRHip[club][3]) / 30 * spare
        xx = 1-2*(y*y+z*z)
        xy = 2*(x*y - z*w)
        xz = 2*(x*z+y*w)
        yx = 2*(x*y+z*w)
        yy = 1-2*(x*x+z*z)
        yz = 2*(y*z-x*w)
        zx = 2*(x*z-y*w)
        zy = 2*(y*z+x*w)
        zz = 1-2*(x*x+y*y)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[0][0] = xx
                transform_mat[0][1] = xy
                transform_mat[0][2] = xz
                transform_mat[1][0] = yx
                transform_mat[1][1] = yy
                transform_mat[1][2] = yz
                transform_mat[2][0] = zx
                transform_mat[2][1] = zy
                transform_mat[2][2] = zz
        with open(args.bone, 'w') as file:
            json.dump(data, file)

    x11 = width1 // 2
    y11 = int(2 * height1 / 5)
    height_diff = (y11 - upperpoint[1]) / height1
    width_diff = (x11 - upperpoint[0]) / width1
    calc_json_values("Root", x_position)
    calc_json_values("Root1", height_diff)
    calc_json_values("Root2", width_diff)

    angle_deg -= 180
    if angle_deg < 0:
        angle_deg += 360
    if angle_deg >= 360:
        angle_deg -= 360

    json_rotate(rotate_angle, angle_deg)
    bonefile = image_path.split('.')[0] + '.json'
    shutil.copy(args.bone, "scene_" + str(cnt) + "_animations/" + bonefile)
    values = {
        "body_height": height_diff,
        "body_width": width_diff,
        "body angle": angle_deg,
        "position": x_position,
        "RightShoulder": rightshoulder,
        "LeftShoulder": left_shoulder,
        "RHipJoint": angle_joint_left_leg,
        "LHipJoint": angle_joint_right_leg,
        "RightArm": right_arm1,
        "LeftArm": left_arm1,
        "RightLeg": right_leg1,
        "LeftLeg": left_leg1
    }
    with open('scene_' + str(cnt) + '_animations/1.txt', 'w') as file:
        for key, value in values.items():
            file.write(f"{key}: {value}\n")
    os.remove(image_path)
    # cv2.imshow("here", image)
    # cv2.waitKey(0)
directories = os.listdir()
cnt = 0
for directory in directories:
    if "animations" in directory:
        cnt = cnt + 1

if os.path.exists('scene_' + str(cnt) + '_animations'):
    shutil.rmtree('scene_' + str(cnt) + '_animations')
os.mkdir('scene_' + str(cnt) + '_animations')

png_files = glob.glob("*.png")
png_files.sort(key=lambda x: x.split(".")[0])

for png_file in png_files:
    if (png_file.split(".")[0]) != 'logo':
        image_path = png_file
        find_corners(image_path)


   


