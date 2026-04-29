import os
import re
import pandas as pd

path = "output/MP_ID"
df_list = []
for id in range(0, 1000, 100):
    file_name = "MP_ID_"+str(id)+".csv"
    file_path = os.path.join(path, file_name)
    df_list.append(pd.read_csv(file_path, sep=";"))
    
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv("output/MP_ID_all.csv", header=True, index=False, mode="w",sep=";")