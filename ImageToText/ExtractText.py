from PIL import Image
import pytesseract
import numpy as np
import cv2

#set path to tesseract
pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract-OCR\\tesseract'

#read in the image
img = cv2.imread('label5.png')

#convert image to grayscale and blur it
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray =  cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.bilateralFilter(gray,8,255,255)

#show grayed and blurred image
cv2.imshow("Gray", gray)
cv2.waitKey(0)

#detect edges in the image
edged = cv2.Canny(gray, 10, 250)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

cv2.imwrite('newimg.png', gray)

#get text from image
print(pytesseract.image_to_string(Image.open('newimg.png')))