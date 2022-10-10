# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ### 最新PDFを末尾に出力

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import time
from tqdm.notebook import tqdm
import os

OLDEST_YEAR = 2001
LATEST_YEAR  = dt.today().year
YEARS = [y for y in range(OLDEST_YEAR,LATEST_YEAR + 1)]

PDF_BASE_URL = 'https://www.data.jma.go.jp/yoho/typhoon/position_table/'

TYPHOON_NUMS = {}

PDF_URLS = [PDF_BASE_URL + 'table%d.html' % y for y in YEARS]


def getPdfLinks(URL):
    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, 'html.parser')
    ex_pdfs = []
    for c in soup.find_all('ul', class_='contentslink'):
        lis = c.find_all('a')
        for l in lis:
            href = l.get('href')
            if href.find('typhoon') >= 0:
                ex_pdfs.append(l.get('href').replace('../../',''))
    ex_pdfs.sort()
    return ex_pdfs


all_pdf_links = []
for p in tqdm(PDF_URLS):
    ex_pdfs = getPdfLinks(p)
    all_pdf_links.append(ex_pdfs)
    time.sleep(0.5)

IND_PDF_BASE_URL = 'https://www.data.jma.go.jp/yoho/'

all_ind_url = []
for a in tqdm(all_pdf_links):
    for p in tqdm(a):
        all_ind_url.append(IND_PDF_BASE_URL + p)


def download_files(url,file_dir):
    
    response = requests.get(url)
    
    try:
        response_status = response.raise_for_status()
    except Exception as exc:
        print("Error:{}".format(exc))
    
    if response_status == None:
        file = open(os.path.join(file_dir,os.path.basename(url)),"wb")
        for chunk in response.iter_content(100000):
            file.write(chunk)

        file.close()
        print("ダウンロード・ファイル保存完了")


for u in tqdm(all_ind_url):
    download_files(u, 'pdfs')
    time.sleep(0.5)

download_pdfs = os.listdir('pdfs')
try:
    os.remove('./pdfs/.DS_Store')
except:
    pass
download_pdfs.sort()
'ダウンロード済み最新: 20%s年 %s号'%(download_pdfs[-1][1:3],download_pdfs[-1][3:5])


