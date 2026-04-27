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
url = contents[1]
z = "https://lop.parl.ca/sites/ParlInfo/default/en_CA/People/Profile?personId="+url[0]
driver.get(z)
html_content = driver.page_source
soup = BeautifulSoup(html_content,"html.parser")

name = soup.find(id="PersonTitle").text.strip().replace(";",",").replace("\xa0","")

col1 = []
col2 = []
col1.append("Name")
col2.append(name)

df = pd.DataFrame()

list = soup.find(id="PersonInfo").find_all("label")
for l in list:
    # print(l.text)
    col1.append(l.text.strip().replace(";",",").replace(":","").replace("\xa0",""))

list = soup.find(id="PersonInfo").find_all("span")

# tags:
list_tag = [
    "DateOfBirth",
    "PlaceOfBirth",
    "Occupations",
    "PreferredLanguage",
    "YearsOfServices"
    "MP"
]

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
        print(key, ":", value)

for key, value in data.items():
    df.loc[0, key] = value

# for x in list_tag:
#     print("id:", x)
#     info = soup.find(id = x).text.strip().replace(";",",").replace(":","").replace("\xa0","")
#     print("info:", info)
#     # col2.append(info.text.strip().replace(";",",").replace("\xa0",""))
#     df.loc[0, x] = info

z1 = "".join(url)
# df = pd.DataFrame(col2).T
# rows = pd.DataFrame(col1).T
# df2 = pd.concat([rows, df])
df.to_csv("output/MP_ID_"+z1+".csv", header=True, index=False, mode="w",sep=";")
