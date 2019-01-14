from PIL import Image
from PIL import ImageEnhance
import cv2
from pytesseract import image_to_string
import os
rawPath = 'D:\\test\\Camera'
resultPath = 'D:\\test\\result\\Processed'

def processImage(scourcePath,savePath,area):
   image = Image.open(scourcePath)
   #image = image.convert('1')
   print('We are processing Image')
   image = image.convert('L')
   #area = (300, 300, 1889, 1889) #(left,top,right,bottom)
   image = image.crop(area)
   enhancer = ImageEnhance.Contrast(image)
   newImage = enhancer.enhance(1).save(savePath,dpi=(300,300))
   return newImage

#def cropImage(scourcePath,savePath):
 #   image = cv2.imread(scourcePath)
  #  cropImg = image[305:1889,537:2097] #can also try image.crop Ystart:Yend,Xstart:Xend
   # cv2.imwrite(savePath,cropImg)
    #return cropImg

for file in os.listdir(rawPath):
    imagePath = rawPath + '\\' + file
    savePath = resultPath + '\\' + file
    #donePath = finalPath + '\\' + file
    #area = (1297, 241, 2897, 1497) # smallest area  15/18
    area = (1297, 261, 2597, 1197)  #16/18 including Contact
    area = (1297, 271, 2597, 1197)  # 16/18
    #area = (1297, 241, 2897, 2209) # big area 12/18
    processImage(imagePath,savePath,area)
    #cropImage(savePath,donePath)
    print (image_to_string(Image.open(savePath), lang='eng'))
