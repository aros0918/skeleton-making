import cv2
import numpy as np
import math
import json
xx = 0
xy = 0
xz = 0
yx = 0
yy = 0
yz = 0
zx = 0
zy = 0
zz = 0

def distance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
def calc_angle(point1, point2):
    if point2[1] > point1[1] and point2[0] > point1[0]:
        print("2")
        return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
    if point2[1] <= point1[1] and point2[0] > point1[0]:
        
        print("1")
        return (math.atan((point2[1] - point1[1]) / (point2[0] - point1[0])) / 3.14 * 180)
    if point2[1] > point1[1] and point2[0] < point1[0]:
        print("3")
        return (180 - math.atan((point2[1] - point1[1]) / (point1[0] - point2[0])) / 3.14 * 180)
    if point2[1] <= point1[1] and point2[0] <= point1[0]:
        print("4")
        return (180 + math.atan((point1[1] - point2[1]) / (point1[0] - point2[0])) / 3.14 * 180)
def calc_json_values(part, angle):
    if part == "RightShoulder":
        print("right")
        print(angle)
        with open("bone.json") as file:
            data = json.load(file)
        x = -0.075
        y = 0.067
        z = math.cos((angle+90)/2/180*3.14)
        w = math.sqrt(1-x*x-y*y-z*z)
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
        with open('bone.json', 'w') as file:
            json.dump(data, file)
    if part == "LeftShoulder":
        print("Left")
        print(angle)
        with open("bone.json") as file:
            data = json.load(file)
        x = -0.075
        y = -0.068
        z = math.cos((angle+90)/2/180*3.14)
        w = math.sqrt(1-x*x-y*y-z*z)
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
        with open('bone.json', 'w') as file:
            json.dump(data, file)

def find_corners(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find corners using the Shi-Tomasi corner detection algorithm
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=20, qualityLevel=0.02, minDistance=30)
    # Draw circles at the corner locations on the original image
    body_points = []
    other_points = []
    if corners is not None:
        corners = np.intp(corners)
        for i, corner in enumerate(corners):
            x, y = corner.ravel()
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
              else:
                other_points.append((x, y))
    if body_points[0][1] < body_points[1][1]:
      upperpoint = body_points[0]
      lowerpoint = body_points[1]
    else: 
      upperpoint = body_points[1]
      lowerpoint = body_points[0]
    idx = 0
    # print("upperpoint", upperpoint)
    # print("lowerpoint", lowerpoint)
    cv2.circle(image, upperpoint, 3, (255, 0, 0), -1)
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
   
    angle_left_arm = calc_angle(left_arm, upperpoint)
    angle_right_arm = calc_angle(right_arm, upperpoint)

    calc_json_values("RightShoulder", angle_left_arm)
    calc_json_values("LeftShoulder", angle_right_arm)

    cv2.imshow("Final", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "data/1.png"
find_corners(image_path)