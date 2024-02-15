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
        return (180 + math.atan((point1[1] - point2[1]) / (point1[0] - point2[0])) / 3.14 * 180)
def calc_json_values(part, angle):
    if part == "Root":
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
        x = -0.075
        y = 0.067
        z = math.cos((angle+90)/2/180*3.14)
        w = math.sqrt(math.fabs(1-x*x-y*y-z*z))
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
        x = -0.075
        y = -0.068
        z = math.cos((angle+90)/2/180*3.14)
        w = math.sqrt(math.fabs(1-x*x-y*y-z*z))
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
        initialRHip = [[0.067, 0.011, -0.997, 0.001], [0.066, 0.011, -0.974, 0.214], [0.059, 0.01, -0.871, 0.487],
                    [0.046, 0.007, -0.699, 0.714], [0.033, 0.005, -0.493, 0.869], [0.016, 0.002, -0.235, 0.972],
                    [0, 0, 0, 1], [-0.014, -0.002, 0.215, 0.976], [-0.031, -0.005, 0.467, 0.883], [-0.048, -0.008, 0.711, 0.701], [-0.056, -0.009, 0.839, 0.539], [-0.064, -0.011, 0.961, 0.268], [-0.067, -0.011, 0.997, 0.012]
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
        initialRHip = [[-0.084, 0.025, -0.996, 0.004], [-0.081, 0.024, -0.966, 0.244], [-0.073, 0.022, -0.871, 0.485], [-0.06, 0.017, -0.707, 0.704], [-0.043, 0.012, -0.508, 0.86], [-0.021, 0.006, -0.243, 0.97], [0, 0, 0, 1], [0.019, -0.006, 0.228, 0.973], [0.04, -0.012, 0.472, 0.88], [0.059, -0.017,  0.703, 0.708], [0.073, -0.022, 0.867, 0.49], [0.081, -0.024, 0.971, 0.22], [0.084, -0.025, 0.996, 0.05]
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
        initialRHip = [[0.569, -0.023, 0.778, -0.144], [0.586, -0.358, 0.724, 0.058], [0.568, -0.468, 0.628, 0.251],
                    [0.507, -0.558, 0.476, 0.454], [0.417, -0.606, 0.304, 0.605], [0.292, -0.613, 0.1, 0.726],
                    [0.144, -0.576, -0.0115, 0.796]
                    ]
        if angle <= -90:
            angle = -89
        if angle >= 90:
            angle = 89
        angle = angle + 90
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
        initialLHip = [[0.15, 0.578, 0.1, 0.794], [0.29, 0.614, -0.09, 0.718], [0.43, 0.602, -0.33, 0.582],
                    [0.509, 0.556, -0.482, 0.446], [0.568, 0.468, -0.629, 0.253], [0.586, 0.034, -0.738, 0.023],
                    [0.564, 0.203, -0.782, -0.168]
                    ]
        if angle <= 90:
            angle = 91
        if angle >= 270:
            angle = 269
        angle = angle - 90
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
    image = main_image[10:height, 10:width]
    
    directions = [(-1,1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]

    red_points = np.where((image == [0, 0, 255]).all(axis = -1))  # Array of red points
    image[red_points] = [255, 255, 255]

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


            # different = []
            # for dot in black_dots:
            #     dx, dy = dot[0] - x, dot[1] - y
            #     different.append((dx, dy))
            # direction = set()
        
            # for item in different:
            #     if item[0] >= 0 and item[1] >= 0:
            #         direction.add(1)
            #     if item[0] >= 0 and item[1] < 0:
            #         direction.add(2)
            #     if item[0] < 0 and item[1] >= 0:
            #         direction.add(3)
            #     if item[0] < 0 and item[1] < 0:
            #         direction.add(4)
            # print(black_dots)
            # Draw a circle at the corner location
            if len(black_dots) != 2:
                if len(black_dots) > 2:
                    body_points.append((x, y))
                    # cv2.circle(image, (x, y), 3, (255, 0, 0), -1)
                else:
                    other_points.append((x, y))
                    # cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            else:
                joint_points.append((x, y))
                # cv2.circle(image, (x, y), 3, (0, 0, 255), -1)s


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
    # idx = 0
    # print(upperpoint)
    # print(lowerpoint)
    # cv2.circle(image, upperpoint, 3, (255, 0, 0), -1)
    # cv2.circle(image, lowerpoint, 3, (255, 0, 0), -1)

    endpoints = [endpoint for endpoint in endpoints if not (distance(endpoint, upperpoint) <= 40 or distance(endpoint, lowerpoint) <= 40)]
    
    joint_points = [joint_point for joint_point in joint_points if not (distance(joint_point, upperpoint) <= 40 or distance(joint_point, lowerpoint) <= 40)]
    for joint_point in joint_points:
        endpoints = [endpoint for endpoint in endpoints if not (distance(endpoint, joint_point) <= 40)]
    
    # for endpoint in endpoints:
        # cv2.circle(image, endpoint, 5, (255, 255, 0), -1)
        
    if len(endpoints) <= 4:
        return
    while len(endpoints) > 5:
        del endpoints[-1]
    
#     print(endpoints)
#     # Print the endpoints
#     # accuracy 100%
    # print("body points")
    # print(body_points)

    # print("other points")
    # print(other_points)
    if len(other_points) != 5:
        if len(endpoints) == 5:
            other_points.clear()
            other_points = endpoints

    maxdistance = distance(lowerpoint, other_points[0]) - distance(upperpoint, other_points[0])
    idx = 0
    for i in range(len(other_points)):
      if maxdistance < distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i]):
        maxdistance = distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i])
        idx = i
    head_point = other_points[idx]
    #head_point
    # cv2.circle(image, head_point, 7, (0, 0, 255), -1)

    for point in other_points:
       if point[0] == head_point[0] and point[1] == head_point[1]:
          other_points.remove(point)
          break
       
    expanded_upper_points = []
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

    def find_parts(start_point):
        # print("---------------------------------")
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
            # print(x, y)

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
    part_points_array = []
    expand_part_points_array = []
    is_arm = []
    is_leg = []
    index = 0
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
    # for point in legs:
    #     cv2.circle(image, point, 7, (122, 122, 0), -1)
    # for point in arms:
    #     cv2.circle(image, point, 7, (122, 122, 0), -1)
    
    if arms[0][0] > arms[1][0]:
        right_arm = arms[0]
        right_arm_num = arms_num[0]
        left_arm = arms[1]
        left_arm_num = arms_num[1]
    else:
        left_arm = arms[0]
        right_arm = arms[1]
        right_arm_num = arms_num[1]
        left_arm_num = arms_num[0]
    if legs[0][0] > legs[1][0]:
        right_leg = legs[0]
        left_leg = legs[1]
        right_leg_num = legs_num[0]
        left_leg_num = legs_num[1]
    else:
        left_leg = legs[0]
        right_leg = legs[1]
        right_leg_num = legs_num[1]
        left_leg_num = legs_num[0]

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

    # for point in joint_points:
    #     cv2.circle(image, point, 7, (0, 200, 0), -1)
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

    angle_left_arm = calc_angle(left_arm, joint_left_arm)
    angle_right_arm = calc_angle(right_arm, joint_right_arm)
    angle_left_leg = calc_angle(left_leg, joint_left_leg)
    angle_right_leg = calc_angle(right_leg, joint_right_leg)

    angle_joint_left_arm = calc_angle(joint_left_arm, upperpoint)
    angle_joint_right_arm = calc_angle(joint_right_arm, upperpoint)
    angle_joint_left_leg = calc_angle(joint_left_leg, lowerpoint)
    angle_joint_right_leg = calc_angle(joint_right_leg, lowerpoint)

    calc_json_values("RightShoulder", angle_joint_left_arm)
    calc_json_values("LeftShoulder", angle_joint_right_arm)
    calc_json_values("RHipJoint", angle_joint_left_leg)
    calc_json_values("LHipJoint", angle_joint_right_leg)

    if angle_joint_left_arm - angle_left_arm <= -180:
        calc_json_values("RightArm", angle_joint_left_arm - angle_left_arm + 360)
    else:
        calc_json_values("RightArm", angle_joint_left_arm - angle_left_arm)

    if angle_joint_left_leg - angle_left_leg <= -180:
        calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg + 360)
    else:
        calc_json_values("RightLeg", angle_joint_left_leg - angle_left_leg)

    if angle_joint_right_arm - angle_right_arm >= 180:
        calc_json_values("LeftArm", angle_joint_right_arm - angle_right_arm - 360)
    else:
        calc_json_values("LeftArm", angle_joint_right_arm - angle_right_arm)
    
    if angle_joint_right_leg - angle_right_leg >= 180:
        calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg - 360)
    else:
        calc_json_values("LeftLeg", angle_joint_right_leg - angle_right_leg)

    if left_arm[0]/2 + right_arm[0]/2 > upperpoint[0]:
        rotate_angle = calc_angle(((int(left_arm[0]/2 + right_arm[0]/2)), int((right_arm[1]/2 + left_arm[1]/2))), head_point)
    else:
        rotate_angle = calc_angle(((int(left_arm[0]/2 + right_arm[0]/2)), int((right_arm[1]/2 + left_arm[1]/2))), upperpoint)
    
    def json_rotate(angle):
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
    calc_json_values("Root", x_position)
    
    json_rotate(rotate_angle)
    
    bonefile = image_path.split('.')[0] + '.json'
    shutil.copy(args.bone, "scene_" + str(cnt) + "_animations/" + bonefile)
    os.remove(image_path)
    # cv2.imshow("here", image)
    # cv2.waitKey(0)
directories = os.listdir()
cnt = 0
for directory in directories:
    if "animations" in directory:
        print(directory)
        cnt = cnt + 1

if os.path.exists('scene_' + str(cnt) + '_animations'):
    shutil.rmtree('scene_' + str(cnt) + '_animations')
os.mkdir('scene_' + str(cnt) + '_animations')

png_files = glob.glob("*.png")
png_files.sort(key=lambda x: x.split(".")[0])

for png_file in png_files:
    if (png_file.split(".")[0]) != 'logo':
        image_path = png_file
        print(image_path)
        find_corners(image_path)
# find_corners("./2.png")


   


