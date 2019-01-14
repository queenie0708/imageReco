import os
import subprocess
import cv2
from time import sleep
from PIL import Image
ret_code, err_msg = subprocess.getstatusoutput('adb shell rm -rf /sdcard/DCIM/Camera/')
print (ret_code,err_msg)
if ret_code == 1:
   print ('return code is int')

a = subprocess.getstatusoutput('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity')
print(a)
sleep(3)
a = subprocess.getstatusoutput('adb shell input tap 416 1706')
print(a)
sleep(3)
a = subprocess.check_call('adb pull /sdcard/DCIM/Camera')
print(a)
#image = Image.open(r'D:\test\result\Camera\IMG_20100122_034137.jpg').rotate(270).save(r'D:\test\result\Camera\rotate.jpg')
#bmpImage = image.save(r'D:\test\result\Camera\rotate',"BMP")
#imageRotate = image.rotate(270)
#imageRotate.show()
#output=os.popen('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity')
#print(output.read())
#a = subprocess.check_output('adb pull /sdcard/DCIM/Camera')
#print(a)
