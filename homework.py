import requests
import json
from bs4 import BeautifulSoup

# 宣告參數
url = "https://www.edu.tw/News.aspx?n=9E7AC85F1954DDA8" # 要爬取的網址
dict = []   # 全部資料
input_name = input("輸入欲查詢的單位：")
input_amount = input("輸入欲爬取的文章數量：")

# 判斷 input_amount 是否為數字
try:
    input_amount = int(input_amount)
except:
    raise ValueError("請輸入數字")

# 爬取數量為 input_amount 的文章數
while len(dict) < int(input_amount):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("成功")
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_ = "css_tr")
            for tr in table.find_all("tr")[1:]:
                # 若發布單位名稱與輸入名稱相符就將爬取的資料加入陣列
                if tr.find_next("td").find_next("td").find_next("td").text == input_name :
                    article_dict = {}
                    article_dict["date"] = tr.find_next("td").text
                    article_dict["unit"] = input_name
                    article_dict["title"] = tr.find_next("td").find_next("td").text.replace("\u3000", "").replace("\n", "")
                    href = tr.find("a", class_ = "css_mark").get("href")
                    article_dict["url"] = "https://www.edu.tw/" + href
                    dict.append(article_dict)
                    # 資料筆數與欲查詢筆數相同就跳脫迴圈
                    if len(dict) == int(input_amount):
                        break
            # 找到下一頁的網址並更新 url
            url = "https://www.edu.tw/" + soup.find("a", string = "下一頁")["href"].replace("/./", "")
    except:
        print("請檢查網路連線")
        break

# 根據連結至新聞內文的 url 爬取內文資訊
for i in dict:
    try:
        response = requests.get(i.get("url"))
        if response.status_code == 200:
            print("成功")
            article_dict = {}
            soup = BeautifulSoup(response.text, "html.parser")
            article_result = soup.find("div", class_ = "data_midlle_news_box01").find('dd').text
            data = article_result.split("聯絡人：")[1].split("\xa0\xa0\xa0\xa0電話：")
            article_dict["name"] = data[0]
            article_dict["tel"] = data[1].strip().split(" ")[0]
            i["author"] = article_dict
    except:
        print("請檢查網路連線")
        break

# 若有資料則匯出成 json 檔
if not dict == []:
    print("資料匯出成功")
    with open("%s.json" %input_name, "w", encoding = "utf-8") as file:
        json.dump(dict, file)
else:
    print("查無相關資料")