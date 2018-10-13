'''
This program is for my easy-English translate
Date:2018/10/8
Author:ivan1rufus
'''
import urllib.request
import urllib.parse
import tkinter
import requests
import bs4
import re
import json
from bs4 import BeautifulSoup as Bs


#Already import tkinter, prepare for the gui.
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
/69.0.3497.100 Safari/537.36',
}

#Below is for word translate(dictionary)


def dictGetSoup(word, url= 'https://dict.youdao.com/w/eng/'):
    url += word
    response = requests.get(url, headers=headers)
    #print("返回的网页为:" + response.url)
    soup = Bs(response.text, 'lxml')
    #print(soup)
    return soup

def soupProcess(soup):

    # First we get the basic meanings of our word
    if ord(word[0]) > 256:
        basicShow = chnProcess(soup)
    else:
        basicShow = engProcess(soup)

    return basicShow

def engProcess(soup):
    basicList = re.findall(r"<li>(.*?)</li>", str(soup))
    #print(basicList)
    i = 0
    while True:
       if basicList[i].find('<a') == 0:
           basicList.remove(basicList[i])
       else:
            i += 1
       if i == len(basicList):
            break
    return basicList

def chnProcess(soup):
    basicShow = []

    soup2 = re.findall(r'<ul>(.*?)</ul>', str(soup), re.DOTALL)[0]
    wordGroups = soup2.split('</p>\n<p')
    for eachwordGroup in wordGroups:
        wordGroup = ''
        wordList = []
        wordtype = re.findall(r'(?:<.*>)*(.+)</span>', eachwordGroup)
        if len(wordtype) > 0:
            wordGroup += wordtype[0]
        wordGroup += ' '
        words = re.findall(r'>([^<]*)</a>', eachwordGroup)
        for eachWord in words:
            if not (eachWord.find('中法') != -1 or eachWord.find('中日') != -1 \
               or eachWord.find('中韩') != -1 or eachWord.find('中英') != -1):
                wordGroup += eachWord
                if eachWord != words[-1]:
                    wordGroup += ', '
        if len(wordGroup) != 1:
            basicShow.append(wordGroup)

    return basicShow

def dictionary(word):
    soup = dictGetSoup(word)
    showList = soupProcess(soup)
    show(showList)

def show(showList):
    #Basic process
    toShow = []
    
    toShow.append('基本释义:')
    if len(showList) == 0:
        toShow.append('无')
    toShow.extend(showList)
    toShow.append('')
    
    for eachShow in toShow:
            print(eachShow)





#Below is for translating words


def translate(word, url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'):
    showList = []
    #其实这里用requests包也可以，要注意的是url。实际上接受请求并发送回应的url在Request报文里。
    data = {
    'i': '怎么',
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': '1539356660319',
    'sign': '6607a4e010165e79f83811472a173e77',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_CLICKBUTTION',
    'typoResult': 'false'
    }
    
    data['i'] = word

    data = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers)
    
    response = urllib.request.urlopen(req)
    
    html = response.read().decode('utf-8')
    
    html = json.loads(html)

    showList.append(html['translateResult'][0][0]['tgt'])
    show(showList)

def dictOrTranslate(word):
    if word.count(' ') >= 2:
        translate(word)
    else:
        dictionary(word)

if __name__ == '__main__':
    while True:
        word = input('想翻译啥？<如果想使用翻译功能，请在输入中加入两个或以上的空格>\n')

        if word == 'sb':
            break
        dictOrTranslate(word)
