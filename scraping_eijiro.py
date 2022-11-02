# coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json
import re


def main(spell):
    spell=spell.replace(" ","%20")
    if onlyAlphabet(spell):
        spell = spell.lower()
        url = "https://eow.alc.co.jp/search?q=" + spell
    else:
        url = "https://eow.alc.co.jp/search?q=" + spell
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    source = requests.get(url, headers=headers)
    data = BeautifulSoup(source.content, "html.parser")
    explanation_list = []

    if data.select("#resultsList"):
        if data.select("#resultsList")[0].find("ul"):
            if data.select("#resultsList")[0].find("ul").find("li").find_all("div"):
                for i in range(len(data.select("#resultsList")[0].find("ul").find("li").find_all("div"))):
                    if data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol"):
                        for j in range(len(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol"))):
                            if data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol")[j].find_all("li"):
                                for k in range(len(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol")[j].find_all("li"))):
                                    explanation_list.append(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol")[j].find_all("li")[k].get_text())
                            else:
                                explanation_list.append(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].find_all("ol")[j].get_text())
                    else:
                        explanation_list.append(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].get_text())
                    
    tao = explanation_list
    result1 = []
    for txt in tao:
        result1.append(txt.strip())
    if len(explanation_list) == 0:
        return "(error) this word is not found"
    return result1


def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$') 
    return re_roman.fullmatch(text)


def onlyJa(text):
    re_ja = re.compile(
        r'^[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}$')
    return re_ja.fullmatch(text)


if __name__ == '__main__':
    spell = " ".join(sys.argv[1:]).strip()
    out = main(spell)
    obj = []
    if out == "(error) this word is not found":
        tao = {
            'title': "error",
            'subtitle': "(error) This word is not found",
            'arg': "error"
        }
        obj.append(tao)
    else:
        for idx, i in enumerate(out):
            if "◆" in i:
                i=i[:i.find("◆")]
            if ":" in i:
                if i.find('・')>0:
                    tmp = i.split("・")
                    ken = []
                    tao = ""
                    for k in range(len(tmp)):
                        if onlyAlphabet(tmp[k][0]):
                            ken.append(tao[:-1])
                            tao=tmp[k]
                            tao+="・"
                        else:
                            tao+=tmp[k]
                            tao+="・"
                    if tao != "":
                        ken.append(tao)
                else: 
                    ken = [i]
            else:
                ken = [i]
            if len(ken) > 1:
                for idx, k in enumerate(ken):
                    if onlyAlphabet(spell.split()[0]):
                        if idx == 0:
                            tao = {
                                'title': ken[0],
                                'arg': k
                            }
                        else:
                            u = k.split(":")
                            reibun_j = ""
                            reibun_e = ""
                            if u[0]:
                                for now in u:
                                    if now:
                                        if onlyAlphabet(now[0]) or onlyAlphabet(now[-1]):
                                            reibun_e += now
                                            reibun_e += " "
                                        else:
                                            reibun_j += now
                                
                                tao = {
                                    'title': "  ‣ "+reibun_e,
                                    'subtitle': "    "+reibun_j,
                                    'arg': k
                                }
                            else:
                                continue
                        obj.append(tao)
                    else:
                        print("アルファベットじゃない")
            else:
                tao = {
                    'title': ken[0],
                    'arg': ken[0]
                }
                obj.append(tao)
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))
