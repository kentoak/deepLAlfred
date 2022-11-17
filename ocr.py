import os
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import glob
import json
from PIL import Image
import pyocr
import requests
import random

deepl_auth_key = os.environ["DEEPL_AUTH_KEY"] or ""
screenshot_path = os.environ["SCREENSHOT_PATH"] or ""

pyocr.tesseract.TESSERACT_CMD = os.environ["OCR_PATH"] or r'/usr/local/bin/tesseract'
tools = pyocr.get_available_tools()
tool = tools[0]

list_of_files = glob.glob(screenshot_path) 
latest_file = max(list_of_files, key=os.path.getctime)
img = Image.open(latest_file)

builder = pyocr.builders.TextBuilder(tesseract_layout=6)
text = tool.image_to_string(img, lang="eng", builder=builder)
text = text.replace('\"','\\\"')
text = text.replace('\'',"\\'")
text = text.replace('&','%26')
text = text.replace('\n',' ')


deepl_token=deepl_auth_key

source_lang = 'EN'  
target_lang = 'JA'  
param = {
    'auth_key' : deepl_token,
    'text' : text,
    'source_lang' : source_lang,
    "target_lang": target_lang
}

request = requests.post("https://api-free.deepl.com/v2/translate", data=param)
result = request.json()
resultText = result['translations'][0]['text']
resultText.replace('\\"','\"')
resultText.replace(" ","")
resultText.replace('．','。').replace('，','、')

sts=resultText
cnt = len(sts)
CNT=cnt
start=0
tao=[]
subtex=text
subtex=subtex.replace("\\'","\'")
cnt2=len(subtex)
numForTitle=40
if cnt > numForTitle+1:
    start=0
    tmpStart=start
    startForSubtitle=0
    MM=[]
    numForSubtitle=83
    endend=0
    subtitleFinish=False
    while True:
        numForTitle=40
        cnt-=numForTitle
        cnt2-=numForSubtitle
        if cnt > 0:
            now = sts[start:start+numForTitle]
        else:
            now = sts[start:]
        if cnt2>0:
            endend=numForSubtitle
            for i in range(numForSubtitle):
                if i==0:
                    endbreak=subtex[startForSubtitle+endend-1:startForSubtitle+endend]
                    if endbreak == " ":
                        break
                else:
                    endbreak=subtex[startForSubtitle+endend-1:startForSubtitle+endend]
                    if endbreak == " ":
                        break
                    endend-=1
            nowForSubtitle=subtex[startForSubtitle:startForSubtitle+endend]
        if start == 0:
            if cnt2>0:
                a={"title":now,"arg":sts,"subtitle":nowForSubtitle}
            else:
                a={"title":now,"arg":sts,"subtitle":subtex[startForSubtitle:]}
                subtitleFinish=True
        else:
            if cnt>0:
                if cnt2>0:
                    a={"title":now,"arg":now,"subtitle":nowForSubtitle}
                else:
                    a={"title":now,"arg":now,"subtitle":subtex[startForSubtitle:]}
            else:
                if cnt2>0:
                    a={"title":now,"arg":now,"subtitle":nowForSubtitle}
                else:
                    if tmpStart == start:
                        a={"title":"","arg":"","subtitle":subtex[startForSubtitle:]}
                    else:
                        if subtitleFinish:
                            a={"title":now,"arg":now,"subtitle":""}
                        else:
                            a={"title":now,"arg":now,"subtitle":subtex[startForSubtitle:]}
        startForSubtitle+=endend
        tmpStart=start
        if tmpStart+numForTitle<CNT:
            start=tmpStart+numForTitle
        else:
            start=tmpStart
        tao.append(a)
        if cnt < 0 and cnt2 < 0:
            break
else:
    numForSubtitle=83
    startForSubtitle=0
    if cnt2>numForSubtitle:
        while True:
            cnt2 -= numForSubtitle
            if cnt2>0:
                endend=numForSubtitle
                for i in range(numForSubtitle):
                    if i==0:
                        endbreak=subtex[startForSubtitle+endend-1:startForSubtitle+endend]
                        if endbreak == " ":
                            break
                    else:
                        endbreak=subtex[startForSubtitle+endend-1:startForSubtitle+endend]
                        if endbreak==" ":
                            break
                        endend-=1
                nowForSubtitle=subtex[startForSubtitle:startForSubtitle+endend]
            if cnt2>0:
                a={"title":sts,"arg":sts,"subtitle":nowForSubtitle}
            else:
                a={"title":"","arg":"","subtitle":subtex[startForSubtitle:]}
            startForSubtitle+=endend
            tao.append(a)
            if cnt2 < 0:
                break
    else:
        a={"title":sts,"arg":sts,"subtitle":subtex}
        tao.append(a)

sys.stdout.write(json.dumps({'items': tao}, ensure_ascii=False))

#os.remove(latest_file) #完全削除
#shutil.move(latest_file,'/Users/kt/.Trash/') #ごみ箱へ移動する場合
