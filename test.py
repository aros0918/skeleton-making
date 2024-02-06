import cv2
import numpy as np
import math
import json
import os
import shutil
import glob
import string
import argparse

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

def find_corners(image_path):
    # Read the image
    main_image = cv2.imread(image_path)
    height, width, _ = main_image.shape
    image = main_image[10:height, 10:width]
    

    red_points = np.where((image == [0, 0, 255]).all(axis = -1))  # Array of red points
    image[red_points] = [255, 255, 255]

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find corners using the Shi-Tomasi corner detection algorithm
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.2, minDistance=0)

    # Draw circles at the corner locations on the original image
    body_points = []
    other_points = []
    merged_corners = []
    endpoints = []
    
    #find the endpoints first
    black_points = np.argwhere(gray == 0)  # Array of black points
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
        connections
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
                print("apple")
                endpoints.append((px, py))
    # Print the endpoints
    for point in endpoints:
        px, py = point
        cv2.circle(image, point, 3, (0, 122, 122), -1)

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
            # cv2.circle(image, (x, y), 3, (0, 255, 0), -1)  # Draw a small circle at each endpoint
            nearby_points = []
            for dx in range(-12, 12):
                for dy in range(-12, 12):
                    if dx**2 + dy**2 >= 100:
                        nx, ny = x + dx, y + dy
                        if ny >= 0 and ny < gray.shape[0] and nx >= 0 and nx < gray.shape[1]:
                            nearby_points.append((nx-1, ny+1))
                            nearby_points.append((nx-1, ny))
                            nearby_points.append((nx-1, ny-1))
                            nearby_points.append((nx, ny+1))
                            nearby_points.append((nx, ny))
                            nearby_points.append((nx, ny-1))
                            nearby_points.append((nx+1, ny+1))
                            nearby_points.append((nx+1, ny))
                            nearby_points.append((nx+1, ny-1))
            # Find the black dots from the nearby points
            black_dots = []
            for point in nearby_points:
                px, py = point
                if gray[py, px] == 0:
                    black_dots.append(point)
            # Find the direction factors from the black dots to the (x, y) point
            different = []
            for dot in black_dots:
                dx, dy = dot[0] - x, dot[1] - y
                different.append((dx, dy))
            direction = set()
            for item in different:
                if item[0] >= 0 and item[1] >= 0:
                    direction.add(1)
                if item[0] >= 0 and item[1] < 0:
                    direction.add(2)
                if item[0] < 0 and item[1] >= 0:
                    direction.add(3)
                if item[0] < 0 and item[1] < 0:
                    direction.add(4)
            # Draw a circle at the corner location
            if len(direction) != 2:
              if len(direction) > 2:
                body_points.append((x, y))
                cv2.circle(image, (x, y), 3, (255, 0, 0), -1)

              else:
                other_points.append((x, y))
            else:
                cv2.circle(image, (x, y), 3, (0, 0, 0), -1)
               
    print("endpoints")
    print(endpoints)
    
    #accuracy 100%
    print("body points")
    print(body_points)

    # if len(other_points) != 5:
    #     if len(endpoints) == 5:
    #         other_points.clear()
    #         other_points = endpoints
    print("other points")
    print( )
    if len(body_points) >= 2:
        if body_points[0][1] < body_points[1][1]:
            upperpoint = body_points[0]
            lowerpoint = body_points[1]
        else: 
            upperpoint = body_points[1]
            lowerpoint = body_points[0]
    else:
        upperpoint = (gray.shape[1] / 2, gray.shape[0] / 3)
        lowerpoint = (gray.shape[1] / 2, gray.shape[0] / 3 * 2)
    idx = 0
    cv2.circle(image, upperpoint, 3, (255, 0, 0), -1)
    # print(upperpoint)
    # print(lowerpoint)
    cv2.circle(image, lowerpoint, 3, (255, 0, 0), -1)
    
    max = distance(lowerpoint, other_points[0]) - distance(upperpoint, other_points[0])
    for i in range(len(other_points)):
      if max < distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i]):
        max = distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i])
        idx = i
    head_point = other_points[idx]
    for point in other_points:
       if point[0] == head_point[0] and point[1] == head_point[1]:
          other_points.remove(point)
          break
    left_top = (0, 0)
    right_top = (gray.shape[1], 0)
    left_bottom = (0, gray.shape[0])
    right_bottom = (gray.shape[1], gray.shape[0])
    #left_arm
    idx = 0
    min = distance(left_top, other_points[0])
    for i in range(len(other_points)):
       if min > distance(left_top, other_points[i]):
          min = distance(left_top, other_points[i])
          idx = i
    left_arm = other_points[idx]
    # print("left_arm", left_arm)
    cv2.circle(image, left_arm, 3, (0, 0, 255), -1)

    #left_leg
    idx = 0
    min = distance(left_bottom, other_points[0])
    for i in range(len(other_points)):
       if min > distance(left_bottom, other_points[i]):
          min = distance(left_bottom, other_points[i])
          idx = i
    left_leg = other_points[idx]
    # print("left_leg", left_leg)
    cv2.circle(image, left_leg, 3, (0, 0, 255), -1)

    #right_arm
    idx = 0
    min = distance(right_top, other_points[0])
    for i in range(len(other_points)):
       if min > distance(right_top, other_points[i]):
          min = distance(right_top, other_points[i])
          idx = i
    right_arm = other_points[idx]
    # print("right_arm", right_arm)
    cv2.circle(image, right_arm, 3, (0, 0, 255), -1)

    #right_leg
    idx = 0
    min = distance(right_bottom, other_points[0])
    for i in range(len(other_points)):
       if min > distance(right_bottom, other_points[i]):
          min = distance(right_bottom, other_points[i])
          idx = i
    right_leg = other_points[idx]
    # print("right_leg", right_leg)
    cv2.circle(image, right_leg, 3, (0, 0, 255), -1)

    # print("head_point", head_point)
    cv2.circle(image, head_point, 3, (0, 0, 255), -1)
   

   
    # calc_json_values("RightShoulder", angle_left_arm)
    # calc_json_values("LeftShoulder", angle_right_arm)
    # calc_json_values("RHipJoint", angle_left_leg)
    # calc_json_values("LHipJoint", angle_right_leg)

    # bonefile = image_path.split('.')[0] + '.json'
    # shutil.copy(args.bone, "scene_" + str(cnt) + "_animations/" + bonefile)
    # os.remove(image_path)
    cv2.imshow("here", image)
    cv2.waitKey(0)
# directories = os.listdir()
# cnt = 0
# for directory in directories:
#     if "animations" in directory:
#         print(directory)
#         cnt = cnt + 1

# if os.path.exists('scene_' + str(cnt) + '_animations'):
#     shutil.rmtree('scene_' + str(cnt) + '_animations')
# os.mkdir('scene_' + str(cnt) + '_animations')

# png_files = glob.glob("*.png")
# png_files.sort(key=lambda x: x.split(".")[0])

# for png_file in png_files:
#     if (png_file.split(".")[0]) != 'logo':
#         image_path = png_file
#         print(image_path)
#         find_corners(image_path)
find_corners("./2.png")


   


