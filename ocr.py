import os
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import glob
import json
from PIL import Image
import pyocr
import requests
import random

deepl_auth_key = os.environ["DEEPL_ACCESS_TOKEN"] or ""
screenshot_path = os.environ["SCREENSHOT_PATH"] or ""

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

cnt = len(resultText)
start=0
end=36
tao=[]
u=-1
subtex=text
subtex=subtex.replace("\\'","\'")
while True:
    cnt-=36
    u+=1
    if cnt > 0:
        now = resultText[start:start+end]
    if start == 0:
        a={"title":now,"arg":resultText,"subtitle":subtex[100*u:100*(u+1)]}
    else:
        if cnt > 0:
            a={"title":now,"arg":now,"subtitle":subtex[100*u:100*(u+1)]}
        else:
            a={"title":resultText[start:],"arg":resultText[start:],"subtitle":subtex[100*u:100*(u+1)]}
    start+=36
    tao.append(a)
    if cnt < 0:
        break

sys.stdout.write(json.dumps({'items': tao}, ensure_ascii=False))