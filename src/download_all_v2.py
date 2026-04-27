import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


driver = webdriver.Chrome()
err_repo = pd.DataFrame(columns=["id", "soup"])

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
            continue

    if success:
        return data
    else:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        err_repo.loc[len(err_repo)] = [y, soup]
        return data

list_dic = []
for x in contents[10:30]:
    y = x[0]
    list_dic.append(add_new_info(y))

df = pd.DataFrame()
for n, dic in enumerate(list_dic):
    for key, value in dic.items():
        df.loc[n, key] = value

df.to_csv("output/MP_ID.csv", header=True, index=False, mode="w",sep=";")
if len(err_repo) > 0:
    err_repo.to_csv("output/err_ID.csv", header=True, index=False, mode="w",sep=";")