import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome()

filename = r"input/Link_ID.csv"
contents = []
with open(filename, "r") as f:
    urls = csv.reader(f)
    for line in urls:
        contents.append(line)



def add_new_info(y):
    z = " https://lop.parl.ca/sites/ParlInfo/default/en_CA/People/Profile?personId="+y
    success = False
    for m in range(3):
        try:       
            driver.get(z)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")

            name = soup.find(id="PersonTitle").text.strip().replace(";",",").replace("\xa0","")

            data = {}
            data['Name'] = name
            for li in soup.select("#PersonInfo li"):
                label = li.find("label")
                span = li.find("span")
                
                if label and span:
                    key = label.text.strip().replace(":", "").replace("\xa0","")
                    value = span.text.strip().replace(";",",").replace(":","").replace("\xa0","")
                    
                    if key in data:
                        data[key] = data[key] + "|" + value
                    else:
                        data[key] = value
            
            success = True
            break
            
        except:
            print("页面获取失败，重试中，id:",y)
            continue

    if success:
        return data
    else:
        data = {}
        data["erro"] = y
        return data

list_dic = []

erro_count = 0
stop_index = 0
before_first_erro_len = 0
for x in contents:
    erro_count = 0
    stop_index = 0
    y = x[0]
    dic_temp = add_new_info(y)
    list_dic.append(dic_temp)

    if len(dic_temp) <= 1:
        if erro_count == 0:
            stop_index = contents.index(x)
            before_first_erro_len = len(list_dic)-1
        erro_count += 1
        driver.quit()
        driver = webdriver.Chrome()
    else:
        erro_count = 0

    if erro_count == 3:
        print("连续3次错误，停止程序，列表序号：", stop_index)
        while (len(list_dic) != before_first_erro_len):
            list_dic.pop()
        break
        
df = pd.DataFrame()
for n, dic in enumerate(list_dic):
    for key, value in dic.items():
        df.loc[n, key] = value

if erro_count == 3:
    df.to_csv("output/MP_index_"+str(stop_index)+".csv", header=True, index=False, mode="w",sep=";")
else:
    df.to_csv("output/MP.csv", header=True, index=False, mode="w",sep=";")