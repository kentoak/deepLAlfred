import sys
import json
import re
import requests
from bs4 import BeautifulSoup

def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$')
    return re_roman.fullmatch(text)

def isEijiro(spell):
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
    if explanation_list:
        return True
    else:
        return False

def main(spell):
    if onlyAlphabet(spell):
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
    if data.select(".lejEntry"): 
        if data.select(".Translation"):
            for i in range(len(data.select(".Translation"))):
                if data.select(".Translation")[i].select(".BOXTRAN.TRAN"):
                    continue
                if data.select(".Translation")[i].select(".PRETRANCOM") or data.select(".Translation")[i].select(".COLL"):
                    explanation_list.append(
                        data.select(".Translation")[i].get_text())
                    continue
                tmp = ""
                if data.select(".Translation")[i].select(".TRAN"):
                    for j in range(len(data.select(".Translation")[i].select(".TRAN"))):
                        tmp += data.select(".Translation")[
                            i].select(".TRAN")[j].get_text()
                if tmp:
                    explanation_list.append(tmp)
    if data.select(".ljeEntry"): 
        if data.select(".Subentry"):
            for i in range(len(data.select(".Subentry"))):
                t = ""
                if i == 0:
                    t += data.select(".HWD")[0].get_text()
                t += data.select(".Subentry")[i].get_text()
                explanation_list.append(t)
    if len(explanation_list) == 0:
        if isEijiro(spell):
            word=spell.replace(" ","%20")
            if onlyAlphabet(word):
                word = word.lower()
                url = "https://eow.alc.co.jp/search?q=" + word
            else:
                url = "https://eow.alc.co.jp/search?q=" + word
            tao = {
                'title': spell+" をデータベースへ追加",
                'subtitle': url,
                'arg': spell
            }
        else:
            tao = {
                'title': spell+" をデータベースへ追加",
                'subtitle': spell+" をDeepLで翻訳します",
                'arg': spell
            }
        sys.stdout.write(json.dumps({'items': [tao]}, ensure_ascii=False))
    else:
        tao = {
            'title': spell+" をデータベースへ追加",
            'subtitle': url,
            'arg': url
        }
        sys.stdout.write(json.dumps({'items': [tao]}, ensure_ascii=False))


if __name__ == '__main__':
    spell = ''.join(sys.argv[1:][0]).lstrip().rstrip()
    main(spell)
