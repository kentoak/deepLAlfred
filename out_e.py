import sys
import json
import re
import requests
from bs4 import BeautifulSoup


def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$')
    return re_roman.fullmatch(text)


def main(spell):
    spell=spell.replace(" ","%20")
    if onlyAlphabet(spell[0]) or onlyAlphabet(spell[-1]):
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
    if len(explanation_list) != 0:
        word=spell.replace(" ","%20")
        if onlyAlphabet(word):
            word = word.lower()
            url = "https://eow.alc.co.jp/search?q=" + word
        else:
            url = "https://eow.alc.co.jp/search?q=" + word
        tao = {
            'title': spell+" をデータベースへ追加",
            'subtitle': url,
            'arg': url
        }
    else:
        tao = {
            'title': spell+" をデータベースへ追加",
            'subtitle': spell+" をDeepLで翻訳します",
            'arg': spell
        }
    sys.stdout.write(json.dumps({'items': [tao]}, ensure_ascii=False))


if __name__ == '__main__':
    spell = ''.join(sys.argv[1:][0]).lstrip().rstrip()
    main(spell)
