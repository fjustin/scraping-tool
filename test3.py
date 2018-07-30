


# -*- coding:utf-8 -*-
import httplib2
import imgutil
from googleapiclient.discovery import build
 
# image save path
path = "./rice-img"
# parameters
api_key = "AIzaSyDJ4DTdo-3sE4ps0eZcA8izxbadRmH4nF4"   # APIキー
cse_key = "007105116810696614560:2u--ee6kleo" # 検索エンジンID
query = "rice plant"
service = build("customsearch","v1",developerKey=api_key)
 
imgutil.mkdir(path)
 
page_limit = 10 # 検索ページ数
startIndex = 1
response = []
img_list = []
 
for page in range(0,page_limit):
    try:
        response.append(service.cse().list(
            q=query,            # 検索ワード
            cx=cse_key,         # 検索エンジンID
            lr="lang_ja",       # 言語
            num=10,             # 1回あたりの取得件数（max10）
            start=startIndex,   # 取得開始インデックス
            searchType="image"  # 検索タイプ
        ).execute())
        startIndex = response[page].get("queries").get("nextPage")[0].get("startIndex")
    except Exception as e:
        print(e)
 
for i in range(len(response)):
    if len(response[i]['items']) > 0:
        for j in range(len(response[i]['items'])):
            img_list.append(response[i]['items'][j]['link'])
 
for i in range(len(img_list)):
    http = httplib2.Http(".cache")
    url = img_list[i]
    try:
        imgutil.download_img(path,url)
    except Exception as e:
        print("failed to download image at {}".format(url))
        print(e)
        continue