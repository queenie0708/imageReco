from PIL import Image
from PIL import ImageEnhance
import cv2
from pytesseract import image_to_string
#print (image_to_string(Image.open(r'D:\test\result\Camera\croptry.png')))
#print (image_to_string(Image.open('D:\\test\\cropRadio.png'), lang='eng'))
#print (image_to_string(Image.open(r'D:\test\CropRadio.png')))
#print (image_to_string(Image.open(r'D:\test\Select.png')))
#print (image_to_string(Image.open(r'D:\test\calculatorNumber.png')))
#print (image_to_string(Image.open(r'D:\test\calculatorResult.png')))
#imagePath = 'D:\\test\\result\\Camera\\Torch.jpg'
#image = Image.open(imagePath)
#image = image.convert('L') 
#image = image.convert('1')
#image.rotate(180).save('D:\\test\\result\\Camera\\convertL.jpg')
#enhancer = ImageEnhance.Contrast(Image.open('D:\\test\\result\\Camera\\convertL.jpg'))
#enhancer.enhance(2).save('D:\\test\\result\\Camera\\convertE.jpg')
#print (image_to_string(enhangcer))

def cropImage(scourcePath,savePath):
    image = cv2.imread(scourcePath)
    cropImg = image[305:1889,537:2097] #can also try image.crop Ystart:Yend,Xstart:Xend
    cv2.imwrite(savePath,cropImg)
    return cropImg
pathA = 'D:\\test\\result\\Camera\\convertE.jpg'
pathB = 'D:\\test\\result\\Camera\\convertECroped.jpg'
cropImage(pathA,pathB)
print (image_to_string(Image.open(pathB), lang='eng'))

