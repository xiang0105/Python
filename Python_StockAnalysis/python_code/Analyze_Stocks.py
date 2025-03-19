import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def AnalyzeStoks(tickers):
    # 讀取CSV檔案
    file_path = f"./csv/{tickers}_data.csv"  # 請替換為你的CSV檔案路徑
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # 確保 'Close' 欄位是數字型態
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')

    # 去除 NaN 值
    df = df.dropna(subset=['Close'])

    # 計算技術指標：移動平均線
    df['MA20'] = df['Close'].rolling(window=20).mean()  # 20日移動平均
    df['MA50'] = df['Close'].rolling(window=50).mean()  # 50日移動平均

    # 計算最大回撤 (Dropdown)
    df['Max_Drawdown'] = df['Close'].cummax()  # 計算歷史最高點
    df['Drawdown'] = (df['Close'] - df['Max_Drawdown']) / df['Max_Drawdown'] * 100  # 計算回撤百分比

    # 繪製圖表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # 繪製價格圖表（ax1）
    ax1.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1.5)
    ax1.plot(df.index, df['High'], label='High Price', color='green', linestyle='--')
    ax1.plot(df.index, df['Low'], label='Low Price', color='red', linestyle='--')
    ax1.plot(df.index, df['MA20'], label='20-Day MA', color='red', linestyle='--', linewidth=1.5)
    ax1.plot(df.index, df['MA50'], label='50-Day MA', color='green', linestyle='--', linewidth=1.5)
    ax1.set_title(f'{tickers} ETF Price and Moving Averages', fontsize=16)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # 繪製回撤圖表（ax2）
    ax2.plot(df.index, df['Drawdown'], label='Drawdown (%)', color='purple', linestyle='-.', linewidth=1.5)
    ax2.set_title('Maximum Drawdown (Dropdown)', fontsize=16)
    ax2.set_ylabel('Drawdown (%)', fontsize=12, color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.grid(True)

    # 設定x軸格式
    ax2.set_xlabel('Date', fontsize=12)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 顯示圖表
    plt.tight_layout()
    plt.show()
