import cv2

def preprocess(img):
    img = cv2.GaussianBlur(img, (3,3), 0)
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
