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

# options = webdriver.ChromeOptions()
# options.add_argument("--window-position=-10000,0")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

err_repo = pd.DataFrame(columns=["id", "soup"])

filename = r"input/Link_ID.csv"
contents = []
with open(filename, "r") as f:
    urls = csv.reader(f)
    for line in urls:
        contents.append(line)

url = contents[3]
z = " https://lop.parl.ca/sites/ParlInfo/default/en_CA/People/Profile?personId="+url[0]
driver.get(z)
time.sleep(random.uniform(0.5, 1.5))
html_content = driver.page_source
soup = BeautifulSoup(html_content,"html.parser")
col1 = []
col1.append("Name")
list = soup.find(id="PersonInfo").find_all("label")
for l in list:
    print(l.text)
    col1.append(l.text.strip().replace(";",",").replace("\xa0","").replace(":",""))
rows = pd.DataFrame(col1).T


def add_new_info(y, df):
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
            col = []
            col.append(name)
            list = soup.find(id="PersonInfo").find_all("span")
            filtered = [l for l in list if l.get("id")]
            for l in filtered:
                col.append(l.text.strip().replace(";",",").replace("\xa0",""))
            df1 = pd.DataFrame(col).T
            df_new = pd.concat([df, df1])
            success = True
            break
            
        except:
            continue

    if success:
        return df_new
    else:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        err_repo.loc[len(err_repo)] = [y, soup]
        return df


df = rows.copy()
for x in contents[:10]:
    y = x[0]
    df = add_new_info(y, df)

df.to_csv("output/MP_ID.csv", header=False, index=False, mode="w",sep=";")
if len(err_repo) > 0:
    err_repo.to_csv("output/err_ID.csv", header=True, index=False, mode="w",sep=";")