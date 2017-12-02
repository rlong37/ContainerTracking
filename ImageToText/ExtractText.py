from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

def main():
	#set path to tesseract
	pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract-OCR\\tesseract'

	#read in the image
	img = cv2.imread('D:\\Programming\\Git\\ContainerTracking\\ImageToText\\label2.png')
	
	#initial bilateralFilter parameters
	d = 10
	sigmaColor = 200
	sigmaSpace = 200

	#get text from image
	text = extract(img, d, sigmaColor, sigmaSpace)
	
	#check format of string
	count = 0
	correct = check(text)
	
	while(correct == False):
		if(count == 0):
			#modify settings bilateralFilter parameters for cleaning the image to crop
			d = 8
			sigmaColor = 255
			sigmaSpace = 255
			
			#try to extract text again 
			text = extract(img, d, sigmaColor, sigmaSpace)
			
			#check if text is correct
			correct = check(text)
			count += 1
			
			print("Trying again")
			
		elif(count == 1):
			#modify settings bilateralFilter parameters
			d = 9
			sigmaColor = 150
			sigmaSpace = 150
			
			#try to extract text again 
			text = extract(img, d, sigmaColor, sigmaSpace)
			
			#check if text is correct
			correct = check(text)
			count += 1
			
			print("Trying again")
			
		elif(count == 2):
			#modify settings bilateralFilter parameters
			d = 9
			sigmaColor = 100
			sigmaSpace = 100
			
			#try to extract text again
			text = extract(img, d, sigmaColor, sigmaSpace)
			
			#check if text is correct
			correct = check(text)
			count += 1
			
			print("Trying again")
		
		elif(count == 3):
			print('Could not read text.')
			break
			
	if(correct == True):		
		print(text)


	


def extract(img, d, sigmaColor, sigmaSpace):
	#denoise original img
	cleanIMG = cv2.fastNlMeansDenoisingColored(img)
	
	#convert image to grayscale and blur it
	gray = cv2.cvtColor(cleanIMG, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, d, sigmaColor, sigmaSpace)

	#detect edges in the image
	#this is for finding the bounded rectangle in order to crop
	edged = cv2.Canny(gray, 10, 250)
	
	edgeClean = cv2.bilateralFilter(edged, 11, 50, 50)
	
	#find contours
	edgeClean, contours, hierarchy = cv2.findContours(edgeClean.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours[4]
	
	#find extreme points
	x, y = [], []
	for line in contours:
		for c in line:
			x.append(c[0][0])
			y.append(c[0][1])
		
	x1, x2, y1, y2 = min(x), max(x), min(y), max(y)
	
	#crop image
	cropped = img[y1:y2, x1:x2]
	
	#clean cropped image
	cleanCropped = cv2.fastNlMeansDenoisingColored(cropped)
	
	#convert image to grayscale and blur it
	gCropped = cv2.cvtColor(cleanCropped, cv2.COLOR_BGR2GRAY)
	gCropped = cv2.bilateralFilter(gCropped, 10, 100, 100)
	
	#save modified img
	cv2.imwrite('newimg.png', gCropped)
	
	
	#get text from image and clean string
	text = pytesseract.image_to_string(Image.open('newimg.png'))
	text = text.replace(" ", "")
	cleanedText = text.split("/")
	text = cleanedText[0].split("\n")[0]
	return(text)

	
def check(text):
	#check to see if text follows regex
	regexp = re.compile('^[A-Z0-9]{8}UPS$')
	if regexp.search(text):
		return True
	else:
		return False
	
	
if  __name__ =='__main__':
    main()