import os
import gzip
import xml.etree.ElementTree as ET
import pandas as pd

# 原始資料夾路徑
url = r"C:\Users\56433\OneDrive\桌面\NTUT Data\!公路局路段即時路況動態資訊(v2.0)\GZ"
# 輸出的根資料夾
output_root_folder = r"C:\Users\56433\OneDrive\桌面\NTUT Data\!公路局路段即時路況動態資訊(v2.0)\Output"

# 取得資料夾列表（日期）
file_list = os.listdir(url)

# 遍歷每個日期資料夾（例如 20250323, 20250322 等）
for file in file_list:
    sub_folder = os.path.join(url, file)
    
    # 檢查是否是資料夾，假設資料夾名稱是日期格式
    if os.path.isdir(sub_folder):
        # 目標日期資料夾路徑
        output_folder = os.path.join(output_root_folder, file)

        # 如果目標資料夾不存在，則建立它
        os.makedirs(output_folder, exist_ok=True)

        # 取得該日期資料夾下的所有 .gz 檔案
        sub_file_list = os.listdir(sub_folder)

        for sub_file in sub_file_list:
            # 完整的 .gz 檔案路徑
            gz_path = os.path.join(sub_folder, sub_file)

            # 檢查副檔名是否為 .gz
            if not sub_file.endswith('.gz'):
                continue

            # 解壓後檔名（去掉 .gz）
            xml_filename = sub_file[:-3]
            
            # 解壓後檔案的完整儲存路徑
            xml_path = os.path.join(output_folder, xml_filename)

            print(f"解壓縮：{gz_path} → {xml_path}")

            # 解壓縮 .gz 檔案
            with gzip.open(gz_path, 'rb') as f_in:
                with open(xml_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            # 解析 XML 並轉換為 CSV
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 定義命名空間
            namespaces = {'ns': 'http://traffic.transportdata.tw/standard/traffic/schema/'}

            # 提取所有 <LiveTraffic> 元素
            live_traffic_list = root.findall('.//ns:LiveTraffic', namespaces)

            # 建立資料儲存清單
            data = []

            # 遍歷每個 <LiveTraffic> 元素
            for live_traffic in live_traffic_list:
                # 提取每個欄位的資料
                section_id = live_traffic.find('ns:SectionID', namespaces).text
                travel_time = live_traffic.find('ns:TravelTime', namespaces).text
                travel_speed = live_traffic.find('ns:TravelSpeed', namespaces).text
                CongestionLevelID = live_traffic.find('ns:CongestionLevelID', namespaces).text
                congestion_level = live_traffic.find('ns:CongestionLevel', namespaces).text

                # 儲存該筆資料
                data.append({
                    'SectionID': section_id,
                    'TravelTime': travel_time,
                    'TravelSpeed': travel_speed,
                    'CongestionLevelID': CongestionLevelID,
                    'CongestionLevel': congestion_level
                })

            # 將資料轉換成 DataFrame
            df = pd.DataFrame(data)

            # 儲存為 CSV 檔案
            csv_filename = xml_filename.replace('.xml', '.csv')
            output_csv = os.path.join(output_folder, csv_filename)
            df.to_csv(output_csv, index=False)

print("✅ 所有檔案已解壓並轉換為 CSV 完成！")
