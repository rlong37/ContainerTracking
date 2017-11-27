from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

def main():
	#set path to tesseract
	pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract-OCR\\tesseract'

	#read in the image
	img = cv2.imread('D:\\Programming\\Git\\ContainerTracking\\ImageToText\\label1.png')
	
	#initial bilateralFilter parameters
	d = 8
	sigmaColor = 255
	sigmaSpace = 255

	#get text from image
	text = extract(img, d, sigmaColor, sigmaSpace)
	
	#check format of string
	count = 0
	correct = check(text)
	
	while(correct == False):
		if(count == 0):
			#modify settings bilateralFilter parameters
			d = 8
			sigmaColor = 200
			sigmaSpace = 200
			
			#try to extract text again 
			text = extract(img, d, sigmaColor, sigmaSpace)
			
			#check if text is correct
			correct = check(text)
			count += 1
			
			print("Trying again")
			
		elif(count == 1):
			#modify settings bilateralFilter parameters
			d = 6
			sigmaColor = 255
			sigmaSpace = 255
			
			#try to extract text again 
			text = extract(img, d, sigmaColor, sigmaSpace)
			
			#check if text is correct
			correct = check(text)
			count += 1
			
			print("Trying again")
			
		elif(count == 2):
			#modify settings bilateralFilter parameters
			d = 6
			sigmaColor = 200
			sigmaSpace = 200
			
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
	#convert image to grayscale and blur it
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#gray =  cv2.GaussianBlur(gray, (5, 5), 0)
	gray = cv2.bilateralFilter(gray, d, sigmaColor, sigmaSpace)

	#show grayed and blurred image
	#cv2.imshow("Gray", gray)
	#cv2.waitKey(0)

	#detect edges in the image
	edged = cv2.Canny(gray, 10, 250)
	#cv2.imshow("Edged", edged)
	#cv2.waitKey(0)

	cv2.imwrite('newimg.png', gray)
	
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