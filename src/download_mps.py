import os
from selenium import webdriver
import csv
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# print("Set Working Directory")
# os.chdir("E:\study\S2\Evaluating-Econometric-Methods_data")

driver = webdriver.Chrome()
filename = r"input/Link_ID.csv"
contents = []
with open(filename, "r") as f:
    urls = csv.reader(f)
    for line in urls:
        contents.append(line)
# print(contents[:20])
url = contents[5]
z = "https://lop.parl.ca/sites/ParlInfo/default/en_CA/People/Profile?personId="+url[0]
driver.get(z)
html_content = driver.page_source
soup = BeautifulSoup(html_content,"html.parser")

name = soup.find(id="PersonTitle").text.strip().replace(";",",").replace("\xa0","")

col1 = []
col2 = []
col1.append("Name")
col2.append(name)
list = soup.find(id="PersonInfo").find_all("label")
for l in list:
    # print(l.text)
    col1.append(l.text.strip().replace(";",",").replace("\xa0",""))
list = soup.find(id="PersonInfo").find_all("span")
filtered = [l for l in list if l.get("id")]
for l in filtered:
    print(l.text)
    col2.append(l.text.strip().replace(";",",").replace("\xa0",""))
z1 = "".join(url)
df = pd.DataFrame(col2).T
rows = pd.DataFrame(col1).T
df2 = pd.concat([rows, df])
df2.to_csv("output/MP_ID_"+z1+".csv", header=False, index=False, mode="w",sep=";")

