# Justin Nguyen
# Pull kanji according to the number of strokes till all kanji is extracted

import csv
import requests
import re
import gc
from time import sleep
from bs4 import BeautifulSoup

def searchForPages():
    for i in range (40):
        url = "http://www.kanjipedia.jp/sakuin/soukakusu/{}".format(i)
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            kanjiUrl = str(soup)
            regexKanjiPage = re.compile(r'(\d{10})')
            with open("strokePageNumbers.txt", "a") as num:
                for page in re.findall(regexKanjiPage, kanjiUrl):
                    printer = csv.writer(num)
                    printer.writerow([page])
            print(i)
            
            for j in range (15):
                url = "http://www.kanjipedia.jp/sakuin/soukakusu/{}/{}".format(i,j)
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    kanjiUrl = str(soup)
                    with open("strokePageNumbers.txt", "a") as num:
                        for page in re.findall(regexKanjiPage, kanjiUrl):
                            printer = csv.writer(num)
                            printer.writerow([page])
