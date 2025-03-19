import yfinance as yf
import pandas as pd

def GrabStockData(ticker, start_date, end_date):
    try:
        # 下載股票數據
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # 檢查是否有數據
        if data.empty:
            print(f"未能抓取 {ticker} 的數據，請檢查代碼或日期範圍。")
            return None

        # 添加 Ticker 標記
        data["Ticker"] = ticker
        
        # 重置索引將日期作為欄位
        data = data.reset_index()
        
        return data
    except Exception as e:
        print(f"抓取數據時出現錯誤: {e}")
        return None
    
def SaveToCsv(data, filename):
    # 確認 data 是 DataFrame 類型，並且不是 None
    if data is not None and isinstance(data, pd.DataFrame):
        try:
            data.to_csv(filename, index=False)
            print(f"資料已成功儲存至 {filename}")
        except Exception as e:
            print(f"儲存 CSV 檔案時發生錯誤: {e}")
    else:
        print("無效的資料，無法儲存。")
