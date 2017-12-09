import ExtractText
import time
import cv2
import numpy
import os


def main():
    start_time = time.time()
    picCommand = "fswebcam -r 352x288 -S 20 --no-banner image.jpg"
    #os.system(picCommand)
    img = cv2.imread("label4.png")
    #img = cv2.imread("image.jpg")
    takePictureTime = str(round(time.time() - start_time, 2))
    
    #extract text from label
    start_extract = time.time()
    label, count = ExtractText.readImg(img)
    end_extract = time.time()
    extract_time = str(round(end_extract - start_extract, 2))
    
    cameraid = getMAC()
    finaltime = round((time.time() - start_time), 2)
    
    print("\nContainer: " + label + '\nCamera: ' + cameraid + "\n")
    print("%s seconds to execute entire program" %finaltime)
    print("Program had to try again " + str(count) + " times.")
    print("Took " + takePictureTime + " seconds to take picture.")
    print("Took " + extract_time + " seconds to extract text.")
    cv2.imshow("img", img)
    cv2.waitKey(0)


# Return the MAC address of the specified interface
def getMAC(interface='eth0'):
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

if __name__ =='__main__':
    main()