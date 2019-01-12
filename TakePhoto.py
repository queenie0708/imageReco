import os
import subprocess
import cv2
from time import sleep
from PIL import Image
a = subprocess.check_output('adb shell rm -rf /sdcard/DCIM/Camera/',stderr=subprocess.STDOUT,shell=True)
print(a)
a = subprocess.check_output('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity',stderr=subprocess.STDOUT,shell=True)
print(a)
sleep(3)
a = subprocess.check_output('adb shell input tap 416 1706',stderr=subprocess.STDOUT,shell=True)
print(a)
sleep(3)
a = subprocess.check_output('adb pull /sdcard/DCIM/Camera',stderr=subprocess.STDOUT,shell=True)
print(a)
#image = Image.open(r'D:\test\result\Camera\IMG_20100122_034137.jpg').rotate(270).save(r'D:\test\result\Camera\rotate.jpg')
#bmpImage = image.save(r'D:\test\result\Camera\rotate',"BMP")
#imageRotate = image.rotate(270)
#imageRotate.show()
#output=os.popen('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity')
#print(output.read())
