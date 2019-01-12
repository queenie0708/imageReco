import os
import subprocess
import cv2
import json
from time import sleep
from PIL import Image

def initResultJson(expectString):
    result = {}
    result['code'] = 500
    result['status'] = 'internal error'
    result['data'] = {}
    result['data']['expect'] = expectString
    result['data']['actual'] = []

    result['err_msg'] = ''
    return result

def takePhoto():
    a = subprocess.check_output('adb shell rm -rf /sdcard/DCIM/Camera/',stderr=subprocess.STDOUT,shell=True)
    print(a)
    a = subprocess.check_output('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity',stderr=subprocess.STDOUT,shell=True)
    print(a)
    sleep(3)
    a = subprocess.check_output('adb shell input tap 416 1706',stderr=subprocess.STDOUT,shell=True)
    print(a)
    sleep(5)
    result = subprocess.check_call('adb pull /sdcard/DCIM/Camera',shell=True) #if 0 success
    print(result)
    if result == 0:
        return true
    else:
        return false


def photoRecognise(resultJson):
    rawPath = './Camera'
    resultPath = 'D:\\Processed'
    finalPath = 'D:\\Done'
    if resultPath not in os.listdir('D:\\'):
        os.mkdir(resultPath)
    if finalPath not in os.listdir('D:\\'):
        os.mkdir(finalPath)
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

    processImage(rawPath,resultPath)
    cropImage(savePath,donePath)
    actualResult = image_to_string(Image.open(donePath), lang='eng')
    print (actualResult)
    #resultJson['data']['actual']=[]

    if actualResult :
        if actualResult.Strip() is not None:
            lines = actualResult.split("\r\n")
            lines_stripped = [x.strip() for x in lines]
            resultJson['data']['actual'] = lines_stripped

            if

    #reteurn resutlJson

def _main():
    resultJson=initResultJson()
#    try:
    if takePhoto():
        resultJson = photoRecognise()
    else:
        resultJson = {
            "code" : "500",
            "statues" : "internal error",
            "data" : null,
            "error_msg": "failed to take photo"
                      }
    with open('imageAI.json', 'w') as outfile:
        json.dump(resultJson, outfile)
#    except Error as e:
