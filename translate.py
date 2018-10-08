'''
This program is for my easy-English translate
Date:2018/10/8
Author:ivan1rufus
'''

import requests
import bs4
import re
from bs4 import BeautifulSoup as Bs

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

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
    return re.findall(r"<li>([^(<a)]*?)</li>", str(soup))

def chnProcess(soup):
    basicShow = []
    print(soup)
    soup2 = re.findall(r'<ul>.*</ul>', str(soup))[0]

    wordGroups = soup2.split('</p><p>')
    for eachwordGroup in wordGroups:
        wordGroup = ''
        wordGroup += re.match(r'(?:<.*>)*(.+)</span>', eachwordGroup)
        words = re.findall(r'<.*?>(.+)</a>')
        for eachWord in words:
            wordGroup += eachWord
        basicShow.append(wordGroup)

    return basicShow

def dictionary(word):
    soup = dictGetSoup(word)
    showList = soupProcess(soup)
    for eachShow in showList:
        print(eachShow)

if __name__ == '__main__':
    while True:
        word = input('你又不记得哪个单词了？\n')

        if word == 'sb':
            break
        dictionary(word)