# coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json
import re


def main(spell):
    spell=spell.replace(" ","-")
    if onlyAlphabet(spell[0]) or onlyAlphabet(spell[-1]):
        spell = spell.lower()
        url = "https://www.ldoceonline.com/jp/dictionary/english-japanese/" + spell
    else:
        url = "https://www.ldoceonline.com/jp/dictionary/japanese-english/" + spell
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    source = requests.get(url, headers=headers)
    data = BeautifulSoup(source.content, "html.parser")
    explanation_list = []
    if data.select_one(".lejEntry"):
        if data.select_one(".lejEntry").select_one(".Wordclass"):
            da=data.select_one(".lejEntry").select_one(".Wordclass").get_text()
            #print(da)
            pos,gram,register="","",""
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS"):
                pos=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS").get_text()
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM"):
                gram=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM").get_text()
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels"):
                if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels").select_one(".REGISTER"):
                    register=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels").select_one(".REGISTER").get_text()
            if data.select_one(".lejEntry").select_one(".Wordclass").select(".Lexubox"):
                for k in data.select_one(".lejEntry").select_one(".Wordclass").select(".Lexubox"):
                    if k.select_one(".LEXUINFO"):
                        LEXUINFO=k.select_one(".LEXUINFO").get_text()
                        da=da.replace(LEXUINFO,"")
                    if k.select_one(".LEXUNIT"):
                        LEXUNIT=k.select_one(".LEXUNIT").get_text()
                        da=da.replace(LEXUNIT,"")
                    if k.select_one(".Sense"):
                        if k.select_one(".Sense").select_one(".Translation"):
                            if k.select_one(".Sense").select_one(".Translation").select_one(".BOXTRAN.TRAN"):
                                BOXTRAN=k.select_one(".Sense").select_one(".Translation").select_one(".BOXTRAN.TRAN").get_text()
                                da=da.replace(BOXTRAN,"")
                                #print("BOXTRAN",BOXTRAN)
                        # if k.select_one(".Sense").select_one(".SEMINDINFO"):
                        #     SEMINDINFO=k.select_one(".Sense").select_one(".SEMINDINFO").get_text()
                        #     da=da.replace(SEMINDINFO,"")
                    if k.select_one(".Labels"):
                        Labels=k.select_one(".Labels").get_text()
                        da=da.replace(Labels,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select(".Sense"):
                for k in data.select_one(".lejEntry").select_one(".Wordclass").select(".Sense"):
                    #print(da)
                    if k.select_one(".COLLINFO"):
                        COLLINFO=k.select_one(".COLLINFO").get_text()
                        da=da.replace(COLLINFO,"")
                    if k.select_one(".SEMINDINFO"):
                        SEMINDINFO=k.select_one(".SEMINDINFO").get_text()
                        da=da.replace(SEMINDINFO,"")
                    if k.select_one(".SEMIND"):
                        SEMIND=k.select_one(".SEMIND").get_text()
                        da=da.replace(SEMIND,"")
                    if k.select_one(".GRAM"):
                        GRAM=k.select_one(".GRAM").get_text()
                        da=da.replace(GRAM,"")
                    if k.select_one(".SUBJINFO"):
                        SUBJINFO=k.select_one(".SUBJINFO").get_text()
                        da=da.replace(SUBJINFO,"")
                    if k.select_one(".OBJINFO"):
                        OBJINFO=k.select_one(".OBJINFO").get_text()
                        da=da.replace(OBJINFO,"")
                    if k.select_one(".SUBJINFOTRAN"):
                        SUBJINFOTRAN=k.select_one(".SUBJINFOTRAN").get_text()
                        da=da.replace(SUBJINFOTRAN,"")
                    if k.select_one(".Translation"):
                        if k.select_one(".Translation").select_one(".BOXTRAN.TRAN"):
                            BOXTRAN=k.select_one(".Translation").select_one(".BOXTRAN.TRAN").get_text()
                            da=da.replace(BOXTRAN,"")
                    if k.select(".Patternbox"):
                        for j in k.select(".Patternbox"):
                            if j.select_one(".PATTERN"):
                                PATTERN=j.select_one(".PATTERN").get_text()
                                da=da.replace(PATTERN,"")
                            if j.select_one(".PATTERNPREP"):
                                PATTERNPREP=j.select_one(".PATTERNPREP").get_text()
                                da=da.replace(PATTERNPREP,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select(".Tail"):
                for k in data.select_one(".lejEntry").select_one(".Wordclass").select(".Tail"):
                    Tails=k.get_text()
                    da=da.replace(Tails,"")
            if data.select(".Patternbox"):
                for j in k.select(".Patternbox"):
                    if j.select_one(".PATTERN"):
                        PATTERN=j.select_one(".PATTERN").get_text()
                        da=da.replace(PATTERN,"")
                    if j.select_one(".PATTERNPREP"):
                        PATTERNPREP=j.select_one(".PATTERNPREP").get_text()
                        da=da.replace(PATTERNPREP,"")
            #print("da",da.replace(gram,"").replace(pos,"").replace(register,"").replace("\n","").rstrip().lstrip())
            final=da.replace(gram,"").replace(pos,"").replace(register,"").replace("\n","").rstrip().lstrip()
            #print("final",final)
            explanation_list.append(final)
        
        if len(explanation_list)==0:
            da=""
            gram=""
            if data.select_one(".lejEntry").select(".Phrvsense"):
                for k in data.select_one(".lejEntry").select(".Phrvsense"):
                    da+=k.get_text()
            explanation_list.append(da.replace("\n","").rstrip().lstrip())
            

    if data.select_one(".ljeEntry"):  # 和英
        if data.select_one(".ljeEntry").select_one(".inline.Subentry"):  # 和英
            if data.select_one(".ljeEntry").select_one(".inline.Subentry").select_one(".POS"):
                pos=data.select_one(".ljeEntry").select_one(".inline.Subentry").select_one(".POS").get_text()
            explanation_list.append(data.select_one(".ljeEntry").select_one(".inline.Subentry").get_text().replace(pos,"").replace("\n","").rstrip().lstrip())
    
    tao = explanation_list
    result = ""
    for idx, txt in enumerate(tao):
        if idx < len(tao)-1:
            tmp = tao[idx]
            result += tmp.strip()+", "
        else:
            tmp = tao[idx]
            result += tmp.strip()
    result1 = []
    for txt in tao:
        result1.append(txt.strip())
    if len(explanation_list) == 0:
        return "(error) this word is not found"
    return result1


def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$')  # a-z:小文字、A-Z:大文字
    return re_roman.fullmatch(text)


def onlyJa(text):
    re_ja = re.compile(
        r'^[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}$')
    return re_ja.fullmatch(text)


if __name__ == '__main__':
    spell = " ".join(sys.argv[1:]).strip()
    out1 = main(spell)
    #print(out1)
    out = main(spell)[0]
    obj = []
    if out1 == "(error) this word is not found":
        tao = {
            'title': "error",
            'subtitle': "(error) This word is not found",
            'arg': "error"
        }
        obj.append(tao)
    else:
        #print(len(out))
        if onlyAlphabet(spell[0]):
            #if "  " in i:
            #print(out)
            k=re.compile(r"\d ").split(out) #数字+半角スペース区切りで分割
            #print("k",k)
            #k.pop(0)
            #print(len(k),k)
            #out1="• ".join(k)
            for out1 in k:
                if len(k)==0:
                    continue
                #print("out1",out1)
                if out1.find("成句  →")>=0:
                    out1 = out1[:out1.find("成句  →")]
                if out1.find(" —")>=0:
                    out1 = out1[:out1.find(" —")]
                #print("out1",out1)
                ken = out1.split("• ")
                #print("ken",ken)
                #ken = re.split("[•b]",out1)
                s=[]
                for i in ken:
                    k=i.split("．")
                    for j in k:
                        if j=="   " or j==" ":
                            continue
                        if j:
                            s.append(j)
                ken=s
                if len(ken) > 1:
                    for idx, k in enumerate(ken):
                        #print("k",k)
                        if idx == 0:
                            tao = {
                                'title': ken[0],
                                'arg': k
                            }
                        else:
                            u = k.split(" ")
                            reibun_j = ""
                            reibun_e = ""
                            for i in u:
                                #print("iiiiiiiiii",i)
                                if i:
                                    if onlyAlphabet(i[0]):
                                        reibun_e += i
                                        reibun_e += " "
                                    else:
                                        reibun_j += i
                            if reibun_e and reibun_j:
                                if "b) " in reibun_e:
                                    tao = {
                                        'title': "  "+ reibun_e + reibun_j,
                                        'arg': k
                                    }
                                else:
                                    tao = {
                                        'title': "  ‣ "+reibun_e,
                                        'subtitle': "    "+reibun_j,
                                        'arg': k
                                    }
                        obj.append(tao)
                elif len(ken)==0:
                    continue
                else:
                    tao = {
                        'title': ken[0],
                        'arg': ken[0]
                    }
                    obj.append(tao)
            # else:
            #     ken = out.split("‣")
        #print("ken",ken)
        else:
            #print("out",out)
            k = out.split("‣  ")
            #k.pop(0)
            for out1 in k:
                #print("out1",len(out1),out1)
                ken = out1.split("• ")
                #print("ken",ken)
                if len(ken) > 1:
                    for idx, k in enumerate(ken):
                        if len(k)==0:
                            continue
                        #print("k",k)
                        if " → See English-Japanese Dictionary" in k:
                            k = k.split(" → See English-Japanese Dictionary")[0]
                        #print(k)
                        if idx == 0:
                            tao = {
                                'title': k,
                            }
                        else:
                            # tao = {
                            #     'title': "‣ "+k,
                            #     'subtitle': k.split(" 〘")[0],
                            #     'arg': k.split(" 〘")[0]
                            # }
                            u = k.split(" ")
                            reibun_j = ""
                            reibun_e = ""
                            for i in u:
                                #print("iiiiiiiiii",i)
                                if onlyAlphabet(i):
                                    reibun_e += i
                                    reibun_e += " "
                                else:
                                    reibun_j += i
                            tao = {
                                'title': "  ‣ "+reibun_e,
                                'subtitle': "    "+reibun_j,
                                'arg': k
                            }
                        obj.append(tao)
                elif len(ken) == 0:
                    continue
                else:
                    if not ken[0]:
                        continue
                    #print("len ken",len(ken),ken[0].encode('utf-8'))
                    k=ken[0]
                    if " → See English-Japanese Dictionary " in k:
                        k = k.split(" → See English-Japanese Dictionary ")[0]
                        #print("kkkkkk",k)
                    #print("k=",k)
                    tao = {
                        'title': k,
                        'arg': k
                    }
                    obj.append(tao)
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))
