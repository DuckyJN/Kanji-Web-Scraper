# Justin Nguyen
# Scrapes the kanji from their respective web pages.
# Inefficiently implements regex to replace images with text
# Replaces images of kanji with an image link

import csv
import requests
import re
import gc
import os
import extractKanjiPageNumbers.py
from bs4 import BeautifulSoup

def pullPage():
    with open("strokePageNumbers.txt", "r") as file:
        for i in file:
            url = "http://www.kanjipedia.jp/kanji/{}".format(i).rstrip()
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                kanji = extractKanji(soup)
                readings = extractReadings(soup)
                radical = extractRadical(soup)
                meanings = extractMeanings(soup)

                with open("nooutput.csv", "a", encoding="UTF-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([kanji,readings[0],readings[1],meanings,radical])
            else:
                invalidPage = open("invalidPage.txt", "a")
                invalidPage.write(url + "\n")
                print (url)
                invalidPage.close()
            

def extractKanji(soup):
    findKanji = soup.find("p", id="kanjiOyaji")
    kanjiContainsImg = str(findKanji)
    regexp = re.compile(r'([a-zA-Z0-9_/]+\.png)')
    if regexp.search(kanjiContainsImg):
        findKanji = "http://www.kanjipedia.jp{}".format((regexp.findall(kanjiContainsImg)[0]))
    else:
        findKanji = findKanji.text
    return findKanji

def extractReadings(soup):
    findReadings = soup.find("ul", id="onkunList").text
    formattedReadings = "{}".format(findReadings)
    splitReadings = formattedReadings.split('\n')
    filterReadings = list(filter(None, splitReadings))
    if len(filterReadings) == 1:
        filterReadings.append('')
    return filterReadings

def extractMeanings(soup):
    findMeanings = str(soup.find("div", id="kanjiRightSection"))

    regexpTai = re.compile(r'(<img alt=\"対\" src=\"/common/images/icon_tai\.png\"/>)')
    regexpRui = re.compile(r'(<img alt=\"類\" src=\"/common/images/icon_rui\.png\"/>)')
    regexpHyouki = re.compile(r'(<.*表記*.>)')
    regexpYurai = re.compile(r'(<.*由来*.>)')
    regexpKoji = re.compile(r'(<.*故事*.>)')
    regexpSankou = re.compile(r'(<p c.*参考.*an>)')
    regexpShitatuki = re.compile(r'(<img alt=\"下つき\" src=\"/common/images/icon_shitatsuki\.png\"/>)')
    
    if regexpTai.search(findMeanings):
        findMeanings = re.sub(regexpTai, '（対）', findMeanings)
    if regexpRui.search(findMeanings):
        findMeanings = re.sub(regexpRui, '（類）', findMeanings)
    if regexpHyouki.search(findMeanings):
        findMeanings = re.sub(regexpHyouki, '（表記）', findMeanings)        
    if regexpYurai.search(findMeanings):
        findMeanings = re.sub(regexpYurai, '（由来）', findMeanings)        
    if regexpKoji.search(findMeanings):
        findMeanings = re.sub(regexpKoji, '（故事）', findMeanings)
    if regexpSankou.search(findMeanings):
        findMeanings = re.sub(regexpSankou, '（参考）', findMeanings)
    if regexpShitatuki.search(findMeanings):
        findMeanings = re.sub(regexpShitatuki, '（下つき）', findMeanings)
        
    findMeanings = cleanhtml(findMeanings)
    findMeanings = ' '.join(findMeanings.split())

    return findMeanings
    
def extractRadical(soup):
    findRadical = soup.find("p", "kanjiBushu")
    radicalContainsImg = str(findRadical)
    regexp = re.compile(r'([a-zA-Z0-9_/]+\.png)')
    findRadical = "http://www.kanjipedia.jp{}".format((regexp.findall(radicalContainsImg)[0]))
    return findRadical

# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

extractKanjiPageNumbers.pullPage()
pullPage()
