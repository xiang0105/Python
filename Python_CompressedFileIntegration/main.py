import os
import gzip
import pandas as pd

data_csv = []

# 設定目標資料夾
directory = r"C:\Users\56433\OneDrive\桌面\NTUT Data\!公路局路段即時路況動態資訊(v2.0)\GZ"

# 取得當前工作目錄，作為輸出路徑
current_directory = os.getcwd()

for files in os.listdir(directory):
    for file in os.listdir(directory + "\\" + files):
        with gzip.open(directory + "\\" + files + "\\" + file, 'rb') as f:
            df = pd.read_csv(f, encoding='utf-8')
            data_csv.append(df)

# 合併所有的 DataFrame
data_csv = pd.concat(data_csv, ignore_index=True)

# 設定儲存 CSV 的完整路徑
output_csv_path = os.path.join(current_directory, 'data.csv')

# 儲存合併後的 CSV
data_csv.to_csv(output_csv_path, index=False)

print(f"CSV 文件已儲存到: {output_csv_path}")
