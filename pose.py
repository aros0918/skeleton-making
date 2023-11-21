


import cv2
import numpy as np
image_path = "data/1.png"
def invert_colors(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Invert the colors using bitwise NOT operation
    inverted_image = cv2.bitwise_not(image)
    
    # Display the original and inverted images
    # cv2.imshow("Original Image", image)
    # cv2.imshow("Inverted Image", inverted_image)
    cv2.imwrite("data/middle.png", inverted_image)

# Example usage

invert_colors(image_path)


img = cv2.imread("data/middle.png", cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
skel = np.zeros_like(img, dtype=np.uint8)
temp = np.zeros_like(img, dtype=np.uint8)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
done = False

while not done:
    temp = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
    temp = cv2.bitwise_not(temp)
    temp = cv2.bitwise_and(img, temp)
    skel = cv2.bitwise_or(skel, temp)
    img = cv2.erode(img, element)
    _, max_val, _, _ = cv2.minMaxLoc(img)
    done = (max_val == 0)

cv2.imshow("Skeleton", skel)

skel = cv2.bitwise_not(skel)

# Convert the image to grayscale.


# Apply a corner detection algorithm to the grayscale image.
corners = cv2.goodFeaturesToTrack(skel, maxCorners=30, qualityLevel=0.2, minDistance=5)

# Draw circles at the corner locations on the original image.
if corners is not None:
    corners = np.intp(corners)
    counter = 1
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(skel, (x, y), 5, (0, 255, 0), -1)
        # Add the corner number to the image.
        cv2.putText(skel, str(counter), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        counter += 1

# Show the image with the corners.
cv2.imshow('image', skel)
cv2.waitKey(0)
cv2.destroyAllWindows()

