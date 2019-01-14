import os
import subprocess
import cv2
import json
from time import sleep
from PIL import Image
from PIL import ImageEnhance
from pytesseract import image_to_string
import argparse

def str2bool(v):
    ''' convert yes, true, t, y 1 to boolean True and convert no,false,f,n,0 to boolean False '''
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def d(msg):
    if verbose_flag:
        # print("V: %d %d %s" % (stack()[1].lineno, stack()[2].lineno, msg))
        print("V: %s" % msg)
        sys.stdout.flush()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--expect", required=True, help='what do you expect')
    parser.add_argument('-v', "--verbose", action='store_true',  default=False,  help='output verbose information if specified')
    return parser.parse_args()



def initResultJson(expectString):
    result = {}
    result['code'] = 500
    result['status'] = 'internal error'
    result['data'] = {}
    result['data']['expect'] = expectString
    result['data']['actual'] = []
    result['err_msg'] = ''
    return result

def setResultJson(resultJson,code=None,status=None,actual=None,err_msg=None):
    if code is not None:
        resultJson['code'] = code
    if status is not None:
        resultJson['status'] = status
    if actual is not None:
        resultJson['data']['actual'] = actual
    if err_msg is not None:
        resultJson['err_msg'] = err_msg
    print(resultJson)
    return resultJson

def takePhoto():
    print('we are taking photo')
    ret_code, err_msg = subprocess.getstatusoutput('adb shell rm -rf /sdcard/DCIM/Camera/')
    if ret_code == 0:
        ret_code, err_msg = subprocess.getstatusoutput('adb shell am start -n com.hmdglobal.camera2/com.android.camera.CameraActivity')
        print(ret_code, err_msg)
        if ret_code == 0:
            sleep(3)
            ret_code, err_msg = subprocess.getstatusoutput('adb shell input tap 416 1706')
            sleep(3)
            ret_code, err_msg = subprocess.getstatusoutput('adb shell input tap 416 1706')
            print(ret_code, err_msg)
            if ret_code == 0:
                sleep(5)
                result = subprocess.check_call('adb pull /sdcard/DCIM/Camera')#if 0 success
                print(result)
                if result == 0:
                    return 'true', err_msg
    else:
        return 'false', err_msg


def photoRecognise(resultJson):
    rawPath = './Camera'
    resultPath = 'D:\\Processed'
    #if resultPath not in os.listdir('D:\\'):
        #os.mkdir(resultPath)
    def processImage(scourcePath,savePath,area):
       print('we are processing Image')
       image = Image.open(scourcePath)
       #image = image.convert('1')
       newImage = image.convert('L').rotate(180)
       newImage = newImage.crop(area)
       enhancer = ImageEnhance.Contrast(newImage)
       newImage = enhancer.enhance(1).save(savePath,dpi=(300,300))
       return newImage

    pics = os.listdir(rawPath)
    photoPath = rawPath + '\\' + pics[-1]
    processPath = resultPath + '\\' + pics[-1]
    area = (350, 117, 1573, 979) #left,top,right,bottom
    processImage(photoPath,processPath,area)
    print('image process done')
    actualResult = image_to_string(Image.open(processPath), lang='eng')
    print ('actualResult: ',actualResult)
    if actualResult.strip() != '':
        lines = actualResult.split("\r\n")
        lines_stripped = [x.strip() for x in lines]
        resultJson['data']['actual'] = lines_stripped
        if resultJson['data']['expect'] == resultJson['data']['actual'][0]:
            setResultJson(resultJson,code=200,status='OK')
        else:
            setResultJson(resultJson,code=400,status='not found',err_msg='expect not in actaul')
    else:
        setResultJson(resultJson,code=204,status='find nothing',err_msg='recognised empty string')
    return resultJson

def _main():
   resultJson=initResultJson('') # fill with 500 and internal error
   success = False
   #TODO: handle with excdption if invalide args were passed on
   try:
       global verbose_flag
       args = parse_args()
       if args.verbose:
           verbose_flag = True
       success = True
       print('expect:', args.expect)
       resultJson=initResultJson(args.expect)
   except Exception as e:
       print("e=", e)
       print('500 failed to get expect from -e')
       # output json with except information and exit excution
       print(resultJson)

   print("success : ", success)
   if success:
       success, err_msg = takePhoto()
       print("success in taking photo: ", success)
       if success=='true':
            resultJson = photoRecognise(resultJson)
       else:
            setResultJson(resultJson,code=500,status='internal error',err_msg = err_msg )

   with open('imageAI.json', 'w') as outfile:
       json.dump(resultJson, outfile)
    #    except Error as e:
if __name__ == '__main__':
    _main()
