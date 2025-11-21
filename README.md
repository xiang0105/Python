# Python相關程式

## Python_CompressedFileIntegration

此程式用於整合和處理壓縮檔案，支援多種壓縮格式如ZIP、TAR、GZ等。使用者可以輕鬆地解壓縮和壓縮檔案，並進行相關操作。

### 套件

``` python
import os
import gzip
import xml.etree.ElementTree as ET
import pandas as pd
```

- os: 用於檔案和目錄操作
- gzip: 用於處理GZIP壓縮檔案
- xml.etree.ElementTree: 用於解析XML檔案
- pandas: 用於資料處理和分析

## Python_CrawlerInstance 

此程式用於網頁爬蟲，能夠自動抓取指定網站的內容並進行分析。支援多種網站結構，並能處理動態內容。

### 套件

``` python
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
```

- selenium: 用於自動化瀏覽器操作
- datetime: 用於處理日期和時間
- webdriver: 用於控制瀏覽器
- expected_conditions: 用於等待特定條件
- TimeoutException: 用於處理超時異常
- WebDriverWait: 用於顯式等待
- Service: 用於管理瀏覽器服務
- Options: 用於設定瀏覽器選項
- By: 用於定位元素
- timedelta: 用於時間差計算
- time: 用於時間相關操作

## Python_DataCleaning

此程式用於資料清理和預處理，能夠處理缺失值、重複值和異常值，並進行資料轉換和標準化。

### 套件

``` python
import pandas as pd
```

- read_csv: 用於讀取CSV檔案
- describe: 用於生成資料摘要統計
- dtypes: 用於檢查資料型別
- isnull: 用於檢查缺失值
- dropna: 用於刪除缺失值
- duplicated: 用於檢查重複值
- to_csv: 用於將資料寫入CSV檔案


## Python_Practise

此程式包含各種Python練習範例，涵蓋基礎語法、資料結構、函式和物件導向等主題，適合初學者進行練習和學習。

## Python_Sorted

此程式用於排序資料，支援多種排序演算法如快速排序、合併排序和插入排序。使用者可以根據需求選擇適合的排序方法。

## Python_StatisticsCrawler

此程式用於抓取X網站統計資料，能夠自動從各大統計網站抓取所需的數據，並進行初步分析和整理。

## Python_OpenCV

此程式用於影像處理和電腦視覺，利用OpenCV庫進行圖像的讀取、處理和分析。支援多種影像處理技術如邊緣檢測、物體識別和圖像分割。

### 套件

``` python
import cv2
```

此為OpenCV的預訓練模型檔案，用於人臉偵測：

``` text
haarcascade_frontalface_default.xml
```

- cv2: OpenCV庫，用於影像處理和電腦視覺
- imread: 用於讀取影像檔案
- imshow: 用於顯示影像
- cvtColor: 用於色彩空間轉換
- GaussianBlur: 用於高斯模糊
