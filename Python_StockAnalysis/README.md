# Python Stock Analysis  

一個以 Python 製作的股票分析工具專案，可進行資料抓取、回測、分析與視覺化。

## 專案結構

Python_StockAnalysis/
│
├── csv/ # 原始資料與處理後的 CSV
│ ├── 2330.TW.csv
│ ├── SPY.csv
│ ├── QQQ_data.csv
│ ├── weighted_portfolio.csv
│ └── year_month_return_crosstab.csv
│
├── python_code/ # 核心 Python 程式
│ ├── Analyze_Stocks.py # 股票表現分析
│ ├── Compare_Stocks.py # 多檔股票比較
│ ├── Decentralized_Stocks.py # 分散式投資組合回測
│ ├── Draw_Charts.py # 各類圖表繪製
│ ├── Grab_Stocks.py # 股票資料爬取/下載
│ ├── MonthlyReturnSummary.py # 月報酬統計
│ ├── YearlyReturnBarChart.py # 年報酬柱狀圖
│ └── init.py
│
└── main.py # 主程式（統整並呼叫各模組）

## 功能特色

### 股票資料抓取 (`Grab_Stocks.py`)

- 從指定來源抓取股票價格  
- 存成原始 CSV  
- 支援多檔股票批次抓取  

### 股票基本分析 (`Analyze_Stocks.py`)

- 計算報酬率、波動度  
- 累積報酬  
- 移動平均、趨勢分析  

### 股票比較 (`Compare_Stocks.py`)

- 支援多檔股票績效比較  
- 可繪製不同股票的回測曲線  

### 分散式投資分析 (`Decentralized_Stocks.py`)

- 多資產組合回測  
- 加權投資組合績效  
- 資產配置檢視  

### 圖表繪製 (`Draw_Charts.py`)

- 累積報酬曲線  
- 月報酬 / 年報酬柱狀圖  
- 股票走勢圖  

### 月報酬與年報酬分析

- `MonthlyReturnSummary.py`：計算每月回報  
- `YearlyReturnBarChart.py`：年報酬（Bar Chart）  

---

##　主程式 `main.py`

`main.py` 是專案的執行入口，可用來：

- 選擇分析哪些股票  
- 執行回測  
- 呼叫圖表繪製  
- 產生輸出報表  

## 執行方式

```bash
python main.py
```

## 安裝需求

```　bash
pandas
numpy
matplotlib
yfinance
```
