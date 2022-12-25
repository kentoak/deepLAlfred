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
            pos,gram="",""
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS"):
                pos=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS").get_text()
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM"):
                gram=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM").get_text()
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
            if data.select(".Patternbox"):
                for i in range(len(data.select(".Patternbox"))):
                    da=da.replace(data.select(".Patternbox")[i].get_text(),"")
            explanation_list.append(da.replace(gram,"").replace(pos,""))
        if len(explanation_list)==0:
            da=""
            gram=""
            if data.select_one(".lejEntry").select(".Phrvsense"):
                for k in data.select_one(".lejEntry").select(".Phrvsense"):
                    da+=k.get_text()
            explanation_list.append(da)
            

    if data.select_one(".ljeEntry"):  # 和英
        if data.select_one(".ljeEntry").select_one(".inline.Subentry"):  # 和英
            if data.select_one(".ljeEntry").select_one(".inline.Subentry").select_one(".POS"):
                pos=data.select_one(".ljeEntry").select_one(".inline.Subentry").select_one(".POS").get_text()
            explanation_list.append(data.select_one(".ljeEntry").select_one(".inline.Subentry").get_text().replace(pos,""))
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
    # print(spell)
    # spell = " ".join(spell)  # いち文字目半角スペースなどの対策
    out = main(spell)[0]
    #print(out)
    obj = []
    if out == "(error) this word is not found":
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
            k=re.compile(r"\d ").split(out)
            #print(k)
            k.pop(0)
            #print(len(k),k)
            #out1="• ".join(k)
            for out1 in k:
                #print("out1",out1)
                out1 = out1[:out1.find("成句  →")]
                ken = out1.split("• ")
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
                #print(ken)
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
            k.pop(0)
            for out1 in k:
                #print("out1",len(out1),out1)
                ken = out1.split("• ")
                if len(ken) > 1:
                    for idx, k in enumerate(ken):
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
                else:
                    tao = {
                        'title': ken[0],
                        'arg': ken[0]
                    }
                    obj.append(tao)
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))
