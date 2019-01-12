from PIL import Image
from PIL import ImageEnhance
import cv2
from pytesseract import image_to_string
import os
rawPath = 'D:\\test\\result\\Raw'
resultPath = 'D:\\test\\result\\Processed'
finalPath = 'D:\\test\\result\\done'
def processImage(scourcePath,savePath):
   image = Image.open(scourcePath)
   #image = image.convert('1')
   image = image.convert('L').rotate(180)
   enhancer = ImageEnhance.Contrast(image)
   newImage = enhancer.enhance(1).save(savePath)
   return newImage
   
def cropImage(scourcePath,savePath):
    image = cv2.imread(scourcePath)
    cropImg = image[305:1889,537:2097] #can also try image.crop Ystart:Yend,Xstart:Xend
    cv2.imwrite(savePath,cropImg)
    return cropImg  
    
for file in os.listdir(rawPath):
    imagePath = rawPath + '\\' + file
    savePath = resultPath + '\\' + file
    donePath = finalPath + '\\' + file
    processImage(imagePath,savePath)
    cropImage(savePath,donePath)
    print (image_to_string(Image.open(donePath), lang='eng'))
