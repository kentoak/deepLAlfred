import requests
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import re
import sys
import os
import os.path
import datetime

notion_api_key = os.environ["NOTION_API_KEY"] or ""
notion_database_url = os.environ["NOTION_DATABASE_URL"] or ""
deepl_auth_key = os.environ["DEEPL_AUTH_KEY"] or ""

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
    if data.select(".lejEntry"):  # 英和
        if data.select(".Translation"):
            for i in range(len(data.select(".Translation"))):
                if data.select(".Translation")[i].select(".BOXTRAN.TRAN"):
                    continue
                # 丸括弧#とんがりかっこ
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
    if data.select(".ljeEntry"):  # 和英
        if data.select(".Subentry"):
            for i in range(len(data.select(".Subentry"))):
                t = ""
                if i == 0:
                    t += data.select(".HWD")[0].get_text()
                t += data.select(".Subentry")[i].get_text()
                explanation_list.append(t)
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

def eijiro(word):
    spell=word.replace(" ","%20")
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
                        explanation_list.append(data.select("#resultsList")[0].find("ul").find("li").find_all("div")[i].get_text())
    tao = explanation_list
    result1 = []
    for txt in tao:
        result1.append(txt.strip())
    if len(explanation_list) == 0:
        return "(error) this word is not found"
    return result1

def deepLMeaning(word, onlyAlphabetFlag):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    if onlyAlphabetFlag:
        targetLang = "JA"
    else:
        targetLang = "EN"

    data = {
        "auth_key": deepl_auth_key,
        "text": word,
        "target_lang": targetLang
    }

    result = requests.post(
        'https://api-free.deepl.com/v2/translate', headers=headers, data=data)
    result = result.json()
    if result["translations"]:
        return result["translations"][0]["text"]

meaningList = []
links = []

def format(word, onlyAlphabetFlag, out):
    if out != "(error) this word is not found":
        for idx, i in enumerate(out):
            if onlyAlphabetFlag:
                ken = i.split("• ")
            else:
                ken = i.split("‣")
            if len(ken) > 1:
                for idx, k in enumerate(ken):
                    if onlyAlphabetFlag:
                        if idx == 0:
                            meaningList.append(ken[0])
                    else:
                        if " → See English-Japanese Dictionary" in k:
                            k = k.split(
                                " → See English-Japanese Dictionary")[0]
                        if idx == 0:
                            meaningList.append(ken[0])
            else:
                meaningList.append(ken[0])
    else:
        useEijiro = eijiro(word)
        if useEijiro != "(error) this word is not found":
            spell=word.replace(" ","%20")
            if onlyAlphabet(spell):
                spell = spell.lower()
                url = "https://eow.alc.co.jp/search?q=" + spell
            else:
                url = "https://eow.alc.co.jp/search?q=" + spell
            links.append(url)
            for idx, i in enumerate(useEijiro):
                if ":" in i:
                    ken = i.split("・")
                else:
                    ken = [i]
                meaningList.append(ken[0])
        else:
            meaningList.append(deepLMeaning(word, onlyAlphabetFlag))


def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$') # a-z:小文字、A-Z:大文字
    return re_roman.fullmatch(text[0])


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'


if "https://www.ldoceonline.com/jp/dictionary" in sys.argv[1:][0]:
    link = sys.argv[1:][0]
    word = link[59:]
else:
    link = "なし"
    word = " ".join(sys.argv[1:])
out = main(word)
onlyAlphabet_ = onlyAlphabet(sys.argv[1:][0][0]) or onlyAlphabet(sys.argv[1:][0][-1])
format(word, onlyAlphabet_, out)
if links:
    link=links[0]
headers_for_notion = {"Authorization": f"Bearer {notion_api_key}",
                      "Content-Type": "application/json",
                      "Notion-Version": "2021-05-13"}
databases_ids = [notion_database_url]
databases_id = databases_ids[0][22:][:databases_ids[0][22:].find('?')]
response = requests.request('GET', url=get_request_url(
    f'databases/{databases_id}'), headers=headers_for_notion)
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

now = datetime.datetime.now()

if len(meaningList) >= 7:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Meaning3": {"rich_text": [{"text": {"content": meaningList[2]}}]},
            "Meaning4": {"rich_text": [{"text": {"content": meaningList[3]}}]},
            "Meaning5": {"rich_text": [{"text": {"content": meaningList[4]}}]},
            "Meaning6": {"rich_text": [{"text": {"content": meaningList[5]}}]},
            "Meaning7": {"rich_text": [{"text": {"content": ",".join(meaningList[6:])}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 6:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Meaning3": {"rich_text": [{"text": {"content": meaningList[2]}}]},
            "Meaning4": {"rich_text": [{"text": {"content": meaningList[3]}}]},
            "Meaning5": {"rich_text": [{"text": {"content": meaningList[4]}}]},
            "Meaning6": {"rich_text": [{"text": {"content": meaningList[5]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 5:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Meaning3": {"rich_text": [{"text": {"content": meaningList[2]}}]},
            "Meaning4": {"rich_text": [{"text": {"content": meaningList[3]}}]},
            "Meaning5": {"rich_text": [{"text": {"content": meaningList[4]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 4:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Meaning3": {"rich_text": [{"text": {"content": meaningList[2]}}]},
            "Meaning4": {"rich_text": [{"text": {"content": meaningList[3]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 3:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Meaning3": {"rich_text": [{"text": {"content": meaningList[2]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 2:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Meaning2": {"rich_text": [{"text": {"content": meaningList[1]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
elif len(meaningList) == 1:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Meaning1": {"rich_text": [{"text": {"content": meaningList[0]}}]},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }
else:
    body_for_notion = {
        "parent": {
            "database_id": databases_id
        },
        "properties": {
            "Word": {"title": [{"text": {"content": word}}]},
            "Link": {"url": link},
            "Date": {"rich_text": [{"text": {"content": now.strftime('%Y/%m/%d %H:%M:%S')}}]},
        }
    }

res = requests.request('POST', url=get_request_url(
    'pages'), headers=headers_for_notion, data=json.dumps(body_for_notion))

if res.status_code == 200:
    print("データベースに", word, "を追加しました！")
else:
    print("失敗しました...")
