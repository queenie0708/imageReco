from PIL import Image
from PIL import ImageEnhance
from pytesseract import image_to_string
import os
rawPath = 'D:\\test\\Camera\\files.jpg'
resultPath = 'D:\\test\\result\\Processed\\files.jpg'

def processImage(scourcePath,savePath,area):
       print('we are processing Image')
       image = Image.open(scourcePath)
       #image = image.convert('1')
       newImage = image.convert('L')
       newImage = newImage.crop(area)
       enhancer = ImageEnhance.Contrast(newImage)
       newImage = enhancer.enhance(1).save(savePath,dpi=(300,300))
       return newImage

area = (1297, 241, 2897, 1497) # smallest 
processImage(rawPath,resultPath,area)
