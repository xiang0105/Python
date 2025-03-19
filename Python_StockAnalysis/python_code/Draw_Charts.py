import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.dates as mdates

def DrawChart(tickers):
    try:
        # 初始化空的 DataFrame
        df_empty = pd.DataFrame()

        tickers = [ticker.strip() for ticker in tickers]

        for ticker in tickers:
            # 讀取 CSV 檔案
            df = pd.read_csv(f"./csv/{ticker}_data.csv")

            # 確保 'Date' 欄位轉換為日期格式
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

            # 確保 'Close' 欄位是數字型態
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

            # 去除 NaN 值
            df = df.dropna(subset=['Close'])

            # 只選擇 'Close' 欄位並重新命名
            df = df[['Close']]  # 選擇 Close 欄位
            df = df.rename(columns={"Close": ticker})  # 重命名為 ticker 名稱

            # 合併所有 ETF 資料
            if df_empty.empty:
                df_empty = df
            else:
                # 使用 how='outer' 合併，並且當欄位名稱重複時，加上後綴
                df_empty = df_empty.join(df, how='outer', lsuffix='_left', rsuffix='_right')

        # 繪製股票的收盤價圖表
        plt.figure(figsize=(10, 6))

        # 繪製每個 ETF 的收盤價
        for ticker in tickers:
            plt.plot(df_empty.index, df_empty[ticker], label=ticker)

        # 設定圖表標題與軸標籤
        plt.title(f"ETF Performance Comparison: {', '.join(tickers)}", fontsize=14)
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)

        # 設定 x 軸顯示日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # 顯示滑鼠懸停時的具體價格和日期
        mplcursors.cursor(hover=True)

        # 顯示圖例
        plt.legend()

        # 調整 x 軸標籤顯示角度，避免重疊
        plt.xticks(rotation=45)

        # 自動調整佈局
        plt.tight_layout()

        # 顯示圖表
        plt.show()

    except Exception as e:
        print(f"繪圖時發生錯誤: {e}")
