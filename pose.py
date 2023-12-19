import cv2
import numpy as np
import math
import json
import mediapipe as mp
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
        with open("bone.json") as file:
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
        with open('bone.json', 'w') as file:
            json.dump(data, file)
    if part == "LeftShoulder":
        with open("bone.json") as file:
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
        with open('bone.json', 'w') as file:
            json.dump(data, file)
    if part == "RightUpLeg":
        with open("bone.json") as file:
            data = json.load(file)
        print(angle)
        initialRHip = [[0.499, -0.605, -0.443, 0.435], [0.316, -0.725, -0.325, 0.519], [0.112, -0.794, -0.184, 0.568],
                    [-0.091, -0.809, -0.036, 0.579], [-0.296, -0.771, 0.12, 0.552], [-0.477, -0.68, 0.266, 0.489],
                    [-0.627, -0.546, 0.393, 0.392]
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
            if item['name'] == 'RightUpLeg':
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
    if part == "LeftUpLeg":
        with open("bone.json") as file:
            data = json.load(file)
        print(angle)
        initialLHip = [[-0.625, 0.549, -0.393, 0.392], [-0.472, 0.685, -0.263, 0.488], [-0.287, 0.774, -0.115, 0.552],
                    [-0.082, 0.81, 0.04, 0.579], [0.128, 0.791, 0.193, 0.566], [0.33, 0.718, 0.333, 0.514],
                    [0.505, 0.599, 0.447, 0.429]
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
            if item['name'] == 'LeftUpLeg':
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
        

# Load the image
image = cv2.imread('input/input.png')

# Resize and convert to RGB
image = cv2.resize(image, (640, 480))
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2)

# Process the image
results = pose.process(image_rgb)

# Draw pose landmarks on the image
if results.pose_landmarks:
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                              connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

    # Draw specific landmarks
    landmarks = results.pose_landmarks.landmark
    image_height, image_width, _ = image.shape

    # Left shoulder
    left_shoulder_x = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
    left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
    cv2.circle(image, (left_shoulder_x, left_shoulder_y), 5, (0, 0, 255), -1)
    upperpoint_left = [left_shoulder_x, left_shoulder_y]

    # Right shoulder
    right_shoulder_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width)
    right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)
    cv2.circle(image, (right_shoulder_x, right_shoulder_y), 5, (0, 0, 255), -1)
    upperpoint_right = [right_shoulder_x, right_shoulder_y]

    # Right wrist
    right_wrist_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width)
    right_wrist_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height)
    cv2.circle(image, (right_wrist_x, right_wrist_y), 5, (0, 0, 255), -1)
    right_arm = [right_wrist_x, right_wrist_y]

    # Left wrist
    left_wrist_x = int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width)
    left_wrist_y = int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)
    cv2.circle(image, (left_wrist_x, left_wrist_y), 5, (0, 0, 255), -1)
    left_arm = [left_wrist_x, left_wrist_y]

    # Right hip
    right_hip_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width)
    right_hip_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height)
    cv2.circle(image, (right_hip_x, right_hip_y), 5, (0, 0, 255), -1)
    lowerpoint_right = [right_hip_x, right_hip_y]

    # Left hip
    left_hip_x = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * image_width)
    left_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height)
    cv2.circle(image, (left_hip_x, left_hip_y), 5, (0, 0, 255), -1)
    lowerpoint_left = [left_hip_x, left_hip_y]

    # Right ankle
    right_ankle_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width)
    right_ankle_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height)
    cv2.circle(image, (right_ankle_x, right_ankle_y), 5, (0, 0, 255), -1)
    right_leg = [right_ankle_x, right_ankle_y]

    # Left ankle
    left_ankle_x = int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width)
    left_ankle_y = int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height)
    cv2.circle(image, (left_ankle_x, left_ankle_y), 5, (0, 0, 255), -1)
    left_leg = [left_ankle_x, left_ankle_y]


angle_left_arm = calc_angle(left_arm, upperpoint_left)
angle_right_arm = calc_angle(right_arm, upperpoint_right)
angle_left_leg = calc_angle(left_leg, lowerpoint_left)
angle_right_leg = calc_angle(right_leg, lowerpoint_right)

calc_json_values("RightShoulder", angle_left_arm)
calc_json_values("LeftShoulder", angle_right_arm)
calc_json_values("RightUpLeg", angle_left_leg)
calc_json_values("LeftUpLeg", angle_right_leg)

cv2.imshow("Final", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

