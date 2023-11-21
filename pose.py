# import cv2
# import numpy as np

# # Read the image.
# image = cv2.imread('data/1.png')

# # Convert the image to grayscale.
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply a corner detection algorithm to the grayscale image.
# corners = cv2.goodFeaturesToTrack(gray, maxCorners=30, qualityLevel=0.2, minDistance=5)

# # Draw circles at the corner locations on the original image.
# if corners is not None:
#     corners = np.intp(corners)
#     counter = 1
#     for corner in corners:
#         x, y = corner.ravel()
#         cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
#         # Add the corner number to the image.
#         cv2.putText(image, str(counter), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#         counter += 1

# # Show the image with the corners.
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# # Read the image.
# image = cv2.imread('data/1.png')

# # Convert the image to grayscale.
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply any necessary preprocessing steps, such as blurring or thresholding.
# # For example, you can use Gaussian blur:
# gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # Use HoughCircles to detect circles in the image.
# circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
#                            param1=50, param2=30, minRadius=10, maxRadius=100)

# # Draw the detected circles on the original image.
# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for circle in circles[0, :]:
#         center = (circle[0], circle[1])
#         radius = circle[2]
#         cv2.circle(image, center, radius, (0, 255, 0), 2)

# # Display the image.
# cv2.imshow('Detected Circles', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import numpy as np

# # Read the image.
# image = cv2.imread('data/1.png')

# # Convert the image to grayscale.
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply any necessary preprocessing steps, such as blurring or thresholding.
# # For example, you can use Gaussian blur:
# gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# # Use HoughCircles to detect round objects in the image.
# circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
#                            param1=50, param2=30, minRadius=10, maxRadius=100)

# # Use HoughLines to detect lines in the image.
# edges = cv2.Canny(gray_blurred, 50, 150)
# lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=65)

# # Draw the detected circles on the original image.
# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for circle in circles[0, :]:
#         center = (circle[0], circle[1])
#         radius = circle[2]
#         cv2.circle(image, center, radius, (0, 255, 0), 2)

# # Draw the detected lines on the original image.
# print(len(lines))
# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))
#         cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# # Display the image.
# cv2.imshow('Detected Objects and Lines', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np


# Load the image
image = cv2.imread('data/1.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Detect lines using Hough transform
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# Iterate over the detected lines
for line in lines:
    x1, y1, x2, y2 = line[0]
    
    # Draw the line on the image
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Get the first and last points of the line
    first_point = (x1, y1)
    last_point = (x2, y2)
    
    # Draw circles at the first and last points
    cv2.circle(image, first_point, 5, (255, 0, 0), -1)
    cv2.circle(image, last_point, 5, (0, 0, 255), -1)
    
    # Print the first and last points
    print("First point:", first_point)
    print("Last point:", last_point)

# Display the image with detected lines and points
cv2.imshow("Detected Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
