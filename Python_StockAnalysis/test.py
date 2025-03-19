# import os

# items = os.listdir('csv')
# new_etf = [_[:-4:] for _ in items]

# print(new_etf)

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.dates as mdates
import matplotlib.ticker as ticker  # 匯入額外工具用於格式化

def DrawWeightedChart(tickers, weights , initial_investment , start_date , end_date):
    try:
        if len(tickers) != len(weights):
            raise ValueError("Tickers and weights must have the same length.")

        # 初始化空的 DataFrame
        df_empty = pd.DataFrame()

        # 去除每個 Ticker 的前後空格
        tickers = [ticker.strip() for ticker in tickers]

        for ticker in tickers:
            # 讀取 CSV 檔案
            df = pd.read_csv(f"./csv/{ticker}.csv")

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



        # 計算每個 ETF 的投資
        # 起始日到終點日
        weighted_values = pd.DataFrame(index=df_empty.index)

        # 計算每個 ETF 的加權價值
        for ticker, weight in zip(tickers, weights):
            shares = int((initial_investment * weight) / df_empty[ticker].iloc[0])
            weighted_values[ticker] = shares * df_empty[ticker]  # 加權價值

        # 計算投資組合價值（加權總和）
        weighted_values['Portfolio'] = weighted_values.sum(axis=1)

        # 繪製圖表
        plt.figure(figsize=(12, 8))

        # 各 ETF 收盤價
        for ticker in tickers:
            plt.plot(df_empty.index, df_empty[ticker] * int(initial_investment / df_empty[ticker].iloc[0]), label=f"{ticker} Price")


        # 加權後的投資組合價值
        plt.plot(weighted_values.index, weighted_values['Portfolio'], label="Weighted Portfolio", linewidth=2, linestyle='--')

        # 設定圖表標題與軸標籤
        plt.title(f"ETF Performance with Weighted Portfolio", fontsize=14)
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)

        # 設定 x 軸顯示日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # 顯示滑鼠懸停時的具體價格和日期
        cursor = mplcursors.cursor(hover=True)
        cursor.connect(
            "add", 
            lambda sel: sel.annotation.set_text(
                f"Date: {mdates.num2date(sel.target[0]):%Y-%m-%d}\nPrice: {sel.target[1]:,.2f}"
            )
        )

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

# 使用範例
tickers = ['SPY', 'QQQ', 'VTI']
weights = [0.5, 0.3, 0.2]  # SPY: 50%, QQQ: 30%, VTI: 20%
start_date = '2023-01-01'
end_date = '2023-12-31'
initial_investment = 10000
DrawWeightedChart(tickers, weights , initial_investment , start_date , end_date)
