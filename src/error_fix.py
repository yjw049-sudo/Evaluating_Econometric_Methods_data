import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

df = pd.read_csv("output/MP.csv", sep=";")
erro_list = df["erro"].dropna().tolist()
driver = webdriver.Chrome()
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
for id in erro_list:
    data = add_new_info(str(int(id)))
    index = df[df["erro"] == "some_value"].index
    print(index)
    print(data)
    for key, value in data:
        df.loc[index, key] = value

if df["Name"].isna().any():
    print("NaN exist")
else:
    df.drop(columns=["erro"])
    df.to_csv("output/MP_fixed.csv", header=True, index=False, mode="w",sep=";")
