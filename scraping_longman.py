# coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json
import re
import urllib.parse


def main(spell):
    spell=spell.replace(" ","-")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    if onlyAlphabet(spell[0]) or onlyAlphabet(spell[-1]):
        spell = spell.lower()
        url = "https://www.ldoceonline.com/jp/dictionary/english-japanese/" + spell
        # if requests.get(url, headers=headers)=="":
        #     print(requests.get(url, headers=headers).status_code)
        #     url = "https://www.ldoceonline.com/jp/dictionary/english-japanese/" + spell + "_1"
    else:
        url = "https://www.ldoceonline.com/jp/dictionary/japanese-english/" + spell
    #print(url)
    source = requests.get(url, headers=headers)
    data = BeautifulSoup(source.content, "html.parser")
    if data.select_one(".search_title"):
        data.select_one(".search_title").get_text()=="次のような意味ですか:"
        source = requests.get(url+"_1", headers=headers)
        data = BeautifulSoup(source.content, "html.parser")
    explanation_list = []
    if data.select_one(".lejEntry"):
        if data.select_one(".lejEntry").select_one(".Wordclass"):
            da=data.select_one(".lejEntry").select_one(".Wordclass").get_text()
            #print(da)
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS"):
                pos=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".POS").get_text()
                da=da.replace(pos,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Varbox"):
                Varbox=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Varbox").get_text()
                da=da.replace(Varbox,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM"):
                gram=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".GRAM").get_text()
                da=da.replace(gram,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels"):
                if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels").select_one(".REGISTER"):
                    register=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Labels").select_one(".REGISTER").get_text()
                    da=da.replace(register,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Inflection"):
                Inflection=data.select_one(".lejEntry").select_one(".Wordclass").select_one(".Inflection").get_text()
                da=da.replace(Inflection,"")
            if data.select_one(".lejEntry").select_one(".Wordclass").select(".Lexubox"):
                for k in data.select_one(".lejEntry").select_one(".Wordclass").select(".Lexubox"):
                    if k.select_one(".LEXUINFO"):
                        LEXUINFO=k.select_one(".LEXUINFO").get_text()
                        da=da.replace(LEXUINFO,"")
                    # if k.select_one(".LEXUNIT"):
                    #     LEXUNIT=k.select_one(".LEXUNIT").get_text()
                    #     da=da.replace(LEXUNIT,"")
                    # if k.select(".Sense"):
                    #     for p in k.select(".Sense"):
                    #         if p.select_one(".Translation"):
                    #             if p.select_one(".Translation").select(".BOXTRAN.TRAN"):
                    #                 for q in p.select_one(".Translation").select(".BOXTRAN.TRAN"):
                    #                     BOXTRAN=q.get_text()
                    #                     da=da.replace(BOXTRAN,"")
                    #             if p.select_one(".Translation").select(".TRAN"):
                    #                 for q in p.select_one(".Translation").select(".TRAN"):
                    #                     TRAN=q.get_text()
                    #                     da=da.replace(TRAN,"")
                                    #print("BOXTRAN",BOXTRAN)
                            # if p.select_one(".SEMINDINFO"):
                            #     SEMINDINFO=p.select_one(".SEMINDINFO").get_text()
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
                    # if k.select_one(".SEMIND"):
                    #     SEMIND=k.select_one(".SEMIND").get_text()
                    #     da=da.replace(SEMIND,"")
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
                        # if k.select_one(".Translation").select_one(".FREQTRAN.TRAN"):
                        #     print("sssssssssss",k.select_one(".Translation").select_one(".FREQTRAN.TRAN"))
                    # if k.select(".Patternbox"):
                    #     for j in k.select(".Patternbox"):
                    #         if j.select_one(".PATTERN"):
                    #             PATTERN=j.select_one(".PATTERN").get_text()
                    #             da=da.replace(PATTERN,"")
                    #         if j.select_one(".PATTERNPREP"):
                    #             PATTERNPREP=j.select_one(".PATTERNPREP").get_text()
                    #             da=da.replace(PATTERNPREP,"")
                    #         if j.select(".Sense"):
                    #             for k in j.select(".Sense"):
                    #                 if k.select_one(".Translation"):
                    #                     if k.select_one(".Translation").select(".BOXTRAN.TRAN"):
                    #                         for m in k.select_one(".Translation").select(".BOXTRAN.TRAN"):
                    #                             BOXTRAN=m.get_text()
                    #                             da=da.replace(BOXTRAN,"")
                    #                     if k.select_one(".Translation").select(".TRAN"):
                    #                         for m in k.select_one(".Translation").select(".TRAN"):
                    #                             TRAN=m.get_text()
                    #                             da=da.replace(TRAN,"")
                    if k.select(".inline.Patternbox"):
                        for j in k.select(".inline.Patternbox"):
                            if j.select_one(".PATTERNINFO"):
                                PATTERNINFO=j.select_one(".PATTERNINFO").get_text()
                                da=da.replace(PATTERNINFO,"")
                                #print("tmp10",da)
                #print("tmp1",da)
            if data.select_one(".lejEntry").select_one(".Wordclass").select(".Tail"):
                for k in data.select_one(".lejEntry").select_one(".Wordclass").select(".Tail"):
                    Tails=k.get_text()
                    da=da.replace(Tails,"")
                #print("tmp2",da)
            if data.select("span[class=Patternbox]"): #incline patterboxと区別するためにCSSセレクタにする
                for j in data.select("span[class=Patternbox]"):
                    if j.select_one(".PATTERN"):
                        PATTERN=j.select_one(".PATTERN").get_text()
                        da=da.replace(PATTERN,"")
                        #print("tmp4",da)
                    if j.select_one(".PATTERNPREP"):
                        PATTERNPREP=j.select_one(".PATTERNPREP").get_text()
                        da=da.replace(PATTERNPREP,"")
                        #print("tmp5",da)
                    if j.select_one(".Translation"):
                        if j.select_one(".Translation").select(".BOXTRAN.TRAN"):
                            for m in j.select_one(".Translation").select(".BOXTRAN.TRAN"):
                                BOXTRAN=m.get_text()
                                da=da.replace(BOXTRAN,"")
                        #print("tmp6",da)
                    if j.select(".Sense"):
                        for k in j.select(".Sense"):
                            if k.select_one(".Translation"):
                                if k.select_one(".Translation").select(".BOXTRAN.TRAN"):
                                    for m in k.select_one(".Translation").select(".BOXTRAN.TRAN"):
                                        BOXTRAN=m.get_text()
                                        da=da.replace(BOXTRAN,"")
                                if k.select_one(".Translation"):
                                    if k.select_one(".Translation").select(".TRAN"):
                                        for m in k.select_one(".Translation").select(".TRAN"):
                                            TRAN=m.get_text()
                                            da=da.replace(TRAN,"")
                        #print("tmp7",da)
                #print("tmp8",da)
            #print("da",da.replace(gram,"").replace(pos,"").replace(register,"").replace("\n","").rstrip().lstrip())
            #print("dda",da)
            final=da.replace("\n","").rstrip().lstrip()
            #print("final",final)
            explanation_list.append(final)
        if data.select_one(".lejEntry").select(".Sense"):
            da=""
            for k in data.select_one(".lejEntry").select(".Sense"):   
                da+=k.get_text()
            final=da.replace("\n","").rstrip().lstrip()
            explanation_list.append(final)

        if data.select_one(".lejEntry").select_one(".Head"):
            if data.select_one(".lejEntry").select_one(".Head").select(".Phrvsense"):
                da=""
                gram=""
                explanation_list = []
                for k in data.select_one(".lejEntry").select_one(".Head").select(".Phrvsense"):
                    da+=k.get_text()
                #print(da)
                for k in data.select_one(".lejEntry").select_one(".Head").select(".Phrvsense"):
                    if k.select_one(".boxnum.span"):
                        boxnum=k.select_one(".boxnum.span").get_text()
                        da=da.replace(boxnum,boxnum+" ")
                        #print("da ",da)
                    if k.select_one(".SEMINDINFO"):
                        SEMINDINFO=k.select_one(".SEMINDINFO").get_text()
                        da=da.replace(SEMINDINFO,"")
                    if k.select_one(".OBJINFO"):
                        OBJINFO=k.select_one(".OBJINFO").get_text()
                        da=da.replace(OBJINFO,"")
                #print(da)
                explanation_list.append(da.replace("\n","").rstrip().lstrip())
        # if len(explanation_list)==0:
        #     da=""
        #     gram=""
        #     if data.select_one(".lejEntry").select(".Phrvsense"): #句動詞とか
        #         for k in data.select_one(".lejEntry").select(".Phrvsense"):
        #             da+=k.get_text()
        #         for k in data.select_one(".lejEntry").select(".Phrvsense"):
        #             if k.select_one(".boxnum.span"):
        #                 boxnum=k.select_one(".boxnum.span").get_text()
        #                 da=da.replace(boxnum,boxnum+" ")
        #             if k.select_one(".SEMINDINFO"):
        #                 SEMINDINFO=k.select_one(".SEMINDINFO").get_text()
        #                 da=da.replace(SEMINDINFO,"")

            #print(da)
            #explanation_list.append(da.replace("\n","").rstrip().lstrip())
            

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

def contains_doubleByte_char(text):
    # 正規表現を使用して、文章の中に全角文字が含まれているかどうかを判定する
    if re.search(r'’| / ', text):
        return False
    return bool(re.search(r'[^\x00-\x7F]', text))

if __name__ == '__main__':
    spell = " ".join(sys.argv[1:]).strip()
    out1 = main(spell)
    #print("\nout1 is        \n",out1)
    out = out1[0]
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
            #print("out is          ",out)
            #k=re.compile(r"\d\s[^\x00-\x7F]").split(out) #数字+半角スペース+全角区切りで分割
            #k=re.split(r"(?=\d{2}(?=\d*\s[^\x00-\x7F]))|(?=\d{1,2}\s<)|(?=\d{1,2}\s\s→)|(?=\d(?=\d*\s\s\())|(?=\d+\s\s<)|(?=\d\s\s\sa\))",out) #数字(1回以上の繰り返し)+半角スペース+全角区切りなどで正規表現の先読みをして分割
            #k=re.compile(r"\d{2}(?=\s+\()|\d+(?=\s+\()").split(out)
            pattern=re.compile(r"\d{2}(?=\s+[^\x00-\x7F])|\d{1}(?=\s+[^\x00-\x7F])|\d{2}(?=\s+<)|\d{1}(?=\s+<)|\d{2}(?=\s+→)|\d{2}(?=\s+→)|\d{2}(?=\s+\()|\d{1}(?=\s+\()|\d{2}(?=\s+a\))|\d{1}(?=\s+a\))|\d{2}(?=\s{2}\w)|\d{1}(?=\s{2}\w)")
            k=pattern.split(out)

            # print("len(k)",len(k),"\n")
            # for i in k:
            #     print("kkkk",i)

            #k.pop(0)
            #print(len(k),k)
            #out1="• ".join(k)
            num=0
            for out1 in k:
                if len(k)==0:
                    continue
                #print("out1",out1)
                if not out1:
                    continue
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
                    #k=i.split("．")
                    #print(i)
                    k=re.compile(r"．|(?<=[^\x00-\x7F]\s{2})").split(i)
                    for j in k:
                        #print(j)
                        if j=="   " or j==" ":
                            continue
                        if j:
                            #print(s)
                            s.append(j)
                ken=s
                if len(ken) > 1:
                    for idx, k in enumerate(ken):
                        #print("k",k,"idx",idx)
                        if idx == 0:#番号+意味のところ！
                            num+=1
                            #print("ken[0]",urllib.parse.quote(ken[0][0]))
                            if ken[0][0]==" ":
                                tao = {
                                    'title': str(num)+"."+ken[0],
                                    'arg': k
                                }
                            else:
                                 tao = {
                                    'title': str(num)+". "+ken[0],
                                    'arg': k
                                }
                        else:
                            u = k.split(" ")
                            #print("u",u)
                            reibun_j = ""
                            reibun_e = ""
                            for i in u:
                                if i:
                                    #print("iiiiiiiiii",i)
                                    if i!=",":
                                        #print("iiiii",i)
                                        if not contains_doubleByte_char(i):
                                            reibun_e += i
                                            reibun_e += " "
                                        else:
                                            reibun_j += i
                                        #print("e ",reibun_e)
                                        #print("j ",reibun_j)
                            if reibun_e and reibun_j:
                                if re.match("[a-z]\)\s",reibun_e): #b)など
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
                            else:
                                continue
                        #print("tao",tao)
                        obj.append(tao)
                elif len(ken)==0:
                    continue
                else:#番号+意味のところ！
                    num+=1
                    if ken[0][0]==" ":
                        tao = {
                            'title': str(num)+"."+ken[0],
                            'arg': ken[0]
                        }
                    else:
                        tao = {
                        'title': str(num)+". "+ken[0],
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
