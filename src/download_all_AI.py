import os
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 不开浏览器窗口（更快）
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


driver = create_driver()

# 读取CSV
filename = r"input/Link_ID.csv"
contents = []
with open(filename, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            contents.append(row[0])


def add_new_info(person_id):
    url = f"https://lop.parl.ca/sites/ParlInfo/default/en_CA/People/Profile?personId={person_id}"

    for attempt in range(3):
        try:
            driver.get(url)

            # 等关键元素，而不是body
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "PersonTitle"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            name_tag = soup.find(id="PersonTitle")
            if not name_tag:
                raise ValueError("Name not found")

            data = {}
            data["Name"] = name_tag.text.strip().replace(";", ",").replace("\xa0", "")

            for li in soup.select("#PersonInfo li"):
                label = li.find("label")
                span = li.find("span")

                if label and span:
                    key = label.text.strip().replace(":", "").replace("\xa0", "")
                    value = span.text.strip().replace(";", ",").replace(":", "").replace("\xa0", "")

                    if key in data:
                        data[key] += "|" + value
                    else:
                        data[key] = value

            return data

        except Exception as e:
            print(f"[Retry {attempt+1}/3] 失败 ID={person_id} | {e}")
            time.sleep(2)

    return {"error": person_id}


# 主循环
results = []
error_count = 0
max_consecutive_errors = 3

for idx, person_id in enumerate(contents[:40]):
    result = add_new_info(person_id)

    if "error" in result:
        error_count += 1
    else:
        error_count = 0

    results.append(result)

    # 连续错误停止
    if error_count >= max_consecutive_errors:
        print(f"连续{max_consecutive_errors}次错误，停止在 index={idx}")
        break


driver.quit()

# 转 DataFrame（高效方式）
df = pd.DataFrame(results)

# 保存
output_file = "output/MP_AI.csv" if error_count < max_consecutive_errors else f"output/MP_index_{idx}.csv"
df.to_csv(output_file, index=False, sep=";")

print("完成，保存至:", output_file)