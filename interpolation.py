import numpy as np
import math
import json
import os
import shutil
import glob
import string
import argparse
import sys
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
def calc_json_values(part, angle, path):
    bone_path = path
    if part == "Root":
        with open(bone_path) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][0] = angle
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "Root1":
        with open(bone_path) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][1] = angle
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "Root2":
        with open(bone_path) as file:
            data = json.load(file)
        for item in data:
            if item['name'] == 'Root':
                transform_mat = item['transform_mat']
                transform_mat[3][2] = angle
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "RightShoulder":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "LeftShoulder":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "RightArm":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "RightLeg":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "LeftArm":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "LeftLeg":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "RHipJoint":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)
    if part == "LHipJoint":
        with open(bone_path) as file:
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
        with open(bone_path, 'w') as file:
            json.dump(data, file)


def json_rotate(angle_1, path):

    bone_path = path
   
    with open(bone_path) as file:
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
    with open(bone_path, 'w') as file:
        json.dump(data, file)

directories = os.listdir()
cnt = 0
for directory in directories:
    if "animations" in directory:
        cnt = cnt + 1
average = {}
with open('scene_0_animations/1.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ')
        average[key] = float(value)
for i in range(cnt):
    current_value = {}
    with open('scene_' + str(i) + '_animations/1.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            current_value[key] = float(value)
            if key == 'body_height':
                current_value[key] = float(value) - average['body_height']
            elif key == 'body_width':
                current_value[key] = float(value) - average['body_width']
    with open('scene_' + str(i) + '_animations/1.txt', 'w') as file:
        for key, value in current_value.items():
            file.write(f"{key}: {value}\n")

if cnt == 0:
    sys.exit()
if cnt == 1:
    sys.exit()

for i in range(cnt):
    if i != cnt - 1:
        shutil.copyfile('scene_' + str(i + 1) + '_animations/1.txt', 'scene_' + str(i) + '_animations/2.txt')
        shutil.copyfile('scene_' + str(i + 1) + '_animations/info.txt', 'scene_' + str(i) + '_animations/info.txt')
full_frame_count = 0
for i in range(cnt - 1):
    read_values_first = {}
    read_values_second = {}
    modify = {}
    read_values = {}
    duration = 0
    frame_count = 0

    with open('scene_' + str(i) + '_animations/1.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            read_values_first[key] = float(value)

    with open('scene_' + str(i) + '_animations/2.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            read_values_second[key] = float(value)
            
    modify["body angle"]  = read_values_second["body angle"]
    modify["position"] = read_values_second["position"]
    modify["RightShoulder"] = read_values_second["LeftShoulder"]
    modify["LeftShoulder"] = read_values_second["RightShoulder"]
    if read_values_second["RHipJoint"] - read_values_first["RHipJoint"] > 180:
        modify["RHipJoint"] = read_values_second["RHipJoint"] - 360
    else:
        modify["RHipJoint"] = read_values_second["RHipJoint"]

    if read_values_second["LHipJoint"] - read_values_first["LHipJoint"] > 180:
        modify["LHipJoint"] = read_values_second["LHipJoint"] - 360
    else:
        modify["LHipJoint"] = read_values_second["LHipJoint"]

    # if read_values_second["RightShoulder"] - read_values_first["RightShoulder"] > 180:
    #     modify["RightShoulder"] = read_values_second["RightShoulder"] - 360
    # else:
    #     modify["RightShoulder"] = read_values_second["RightShoulder"]

    # if read_values_second["LeftShoulder"] - read_values_first["LeftShoulder"] > 180:
    #     modify["LeftShoulder"] = read_values_second["LeftShoulder"] - 360
    # else:
    #     modify["LeftShoulder"] = read_values_second["LeftShoulder"]
   
    modify["body_height"] = read_values_second["body_height"]
    modify["body_width"] = read_values_second["body_width"]


    modify["RightArm"] = read_values_second["LeftArm"] + 180
    modify["LeftArm"] = read_values_second["RightArm"] + 180

    # modify["RightArm"] = read_values_second["RightArm"]
    # modify["LeftArm"] = read_values_second["LeftArm"]

    modify["RightLeg"] = read_values_second["RightLeg"]
    modify["LeftLeg"] = read_values_second["LeftLeg"]

    

    with open('scene_' + str(i) + '_animations/info.txt') as file:
        content = file.read()
        parts = content.split()
        duration = int(parts[0])
        frame_count = int(parts[1])
    full_frame_count += frame_count
    if duration == 0:
        duration = 1
    for j in range(duration * 10 + 1):
        shutil.copy(args.bone, 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        bone_path = 'scene_' + str(i) + '_animations/' + str(j) + '.json'
        read_values = {}
        read_values["body angle"] = read_values_first["body angle"] + (modify["body angle"] - read_values_first["body angle"]) / duration / 10 * j
        read_values["position"] = read_values_first["position"] + (modify["position"] - read_values_first["position"]) / duration / 10 * j
        # read_values["RightShoulder"] = read_values_first["RightShoulder"] + (modify["RightShoulder"] - read_values_first["RightShoulder"]) / duration / 10 * j
        # read_values["LeftShoulder"] = read_values_first["LeftShoulder"] + (modify["LeftShoulder"] - read_values_first["LeftShoulder"]) / duration / 10 * j
        read_values["RightShoulder"] = read_values_first["RightShoulder"]
        read_values["LeftShoulder"] = read_values_first["LeftShoulder"]

        read_values["body_height"] = read_values_first["body_height"] + (modify["body_height"] - read_values_first["body_height"]) / duration / 10 * j
        read_values["body_width"] = read_values_first["body_width"] + (modify["body_width"] - read_values_first["body_width"]) / duration / 10 * j

        read_values["RHipJoint"] = read_values_first["RHipJoint"] + (modify["RHipJoint"] - read_values_first["RHipJoint"]) / duration / 10 * j
        read_values["LHipJoint"] = read_values_first["LHipJoint"] + (modify["LHipJoint"] - read_values_first["LHipJoint"]) / duration / 10 * j
        read_values["RightArm"] = read_values_first["RightArm"] + (modify["RightArm"] - read_values_first["RightArm"]) / duration / 10 * j
        read_values["LeftArm"] = read_values_first["LeftArm"] + (modify["LeftArm"] - read_values_first["LeftArm"]) / duration / 10 * j
        # read_values["RightArm"] = read_values_first["RightArm"]
        # read_values["LeftArm"] = read_values_first["LeftArm"]
        read_values["RightLeg"] = read_values_first["RightLeg"] + (modify["RightLeg"] - read_values_first["RightLeg"]) / duration / 10 * j
        read_values["LeftLeg"] = read_values_first["LeftLeg"] + (modify["LeftLeg"] - read_values_first["LeftLeg"]) / duration / 10 * j

        calc_json_values("RightShoulder", read_values["RightShoulder"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("LeftShoulder", read_values["LeftShoulder"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("RHipJoint", read_values["RHipJoint"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("LHipJoint", read_values["LHipJoint"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("RightArm", read_values["RightArm"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("RightLeg", read_values["RightLeg"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("LeftArm", read_values["LeftArm"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("LeftLeg", read_values["LeftLeg"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("Root", read_values["position"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("Root1", read_values["body_height"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')
        calc_json_values("Root2", read_values["body_width"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')

        json_rotate(read_values["body angle"], 'scene_' + str(i) + '_animations/' + str(j) + '.json')

        with open(bone_path) as file:
            data = json.load(file)
        for idx, item in enumerate(data):
        
            if item['name'] == "RightArm":
                if j != 0:
                    item['transform_mat'][3][1] -= 0.2 / duration / 10 * j
                continue
            if item['name'] == "LeftArm":
                if j != 0:
                    item['transform_mat'][3][1] -= 0.2 / duration / 10 * j
                continue
            # if item['name'] == "Root":
            #     if j != 0:
            #         item['transform_mat'][3][2] += 0.3/ duration/ 10 * j    # right and left
            #         item['transform_mat'][3][1] += 0.1/ duration/ 10 * j   #up and down

                # continue
        with open(bone_path, 'w') as outfile:
            json.dump(data, outfile)

with open('./frame_count.txt', 'w') as file:
    file.write(f"{full_frame_count}\n")
os.remove('scene_0_animations/1.txt')
os.remove('scene_0_animations/2.txt')
os.remove('scene_0_animations/info.txt')
if cnt == 2:
    sys.exit()
for i in range(cnt - 2):
    files = os.listdir('scene_0_animations/')
    json_file_count = 0
    for file in files:
        if file.endswith(".json"):
            json_file_count += 1
    files1 = os.listdir('scene_' + str(i + 1) + '_animations/')
    json_file_count1 = 0
    for file in files1:
        if file.endswith(".json"):
            json_file_count1 += 1
    for k in range(json_file_count1):
        shutil.copyfile('scene_' + str(i + 1) + '_animations/' + str(k) + '.json', 'scene_0_animations/' + str(json_file_count + k) + '.json')



    



   


