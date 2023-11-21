import cv2
import numpy as np
def distance(point1, point2):
  return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
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
            # Calculate the number of different direction factors
            print(str(i+1), x, y, len(direction))
            # Draw a circle at the corner location
            if len(direction) != 2:
              
              
              # Add the corner number to the image
              if len(direction) > 2:
                cv2.circle(image, (x, y), 3, (255, 0, 0), -1)
                cv2.putText(image, str(i+1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                body_points.append((x, y))
              else:
                cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
                cv2.putText(image, str(i+1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                other_points.append((x, y))
    if body_points[0][1] < body_points[1][1]:
      upperpoint = body_points[0]
      lowerpoint = body_points[1]
    else: 
      upperpoint = body_points[1]
      lowerpoint = body_points[0]
    idx = 0
    max = distance(lowerpoint, other_points[0]) - distance(upperpoint, other_points[0])
    for i in range(len(other_points)):
      if max < distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i]):
        max = distance(lowerpoint, other_points[i]) - distance(upperpoint, other_points[i])
        idx = i
    head_point = other_points[idx]
    cv2.circle(image, head_point, 3, (0, 255, 0), -1)
    # Display the image with the detected corners
    cv2.imshow("Corners", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "data/1.png"
find_corners(image_path)