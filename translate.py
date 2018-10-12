'''
This program is for my easy-English translate
Date:2018/10/8
Author:ivan1rufus
'''
import tkinter
import requests
import bs4
import re
from bs4 import BeautifulSoup as Bs
#Already import tkinter, prepare for the gui.
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
/69.0.3497.100 Safari/537.36',
}

data = {
'i': '怎么',
'from': 'AUTO',
'to': 'AUTO',
'smartresult': 'dict',
'client': 'fanyideskweb',

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

    showList = []

    #Basic process
    showList.append('基本释义:')
    if len(basicShow) == 0:
        showList.append('无')
    showList.extend(basicShow)
    showList.append('')

    return showList

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
            wordGroup += eachWord
            if eachWord != words[-1]:
                wordGroup += ', '
        basicShow.append(wordGroup)

    return basicShow

def dictionary(word):
    soup = dictGetSoup(word)
    showList = soupProcess(soup)
    for eachShow in showList:
        print(eachShow)





#Below is for translating words


def translate(word, url='http://fanyi.youdao.com/'):
    print('翻译功能正在施工中...\n')
    data['i'] = word
    #print(data)
    response = requests.post(url, headers=headers, data=data)
    #print(response.text)
    print(re.findall(r'<span data-section="0" data-sentence="0" class="">(.*)</span>', response.text)[0])
    pass

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