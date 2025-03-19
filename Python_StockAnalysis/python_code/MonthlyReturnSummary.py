import pandas as pd
import matplotlib.pyplot as plt

def MonthlyReturnSummary():

    # 讀取加權投資組合資料
    df = pd.read_csv(r'csv\weighted_portfolio.csv')

    # 確保 'Date' 欄位是日期格式
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # 確保 'Close' 欄位是數值格式
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # 計算每月的報酬率（以月初和月末的收盤價來計算）
    df['month_start'] = df.groupby(df.index.to_period('M'))['Close'].transform('first')  # 每月第一個交易日的收盤價
    df['month_end'] = df.groupby(df.index.to_period('M'))['Close'].transform('last')  # 每月最後一個交易日的收盤價

    # 計算當月報酬率並將其保留兩位小數
    df['monthly_return'] = ((df['month_end'] - df['month_start']) / df['month_start']) * 100
    df['monthly_return'] = df['monthly_return'].round(2)

    # 添加年份和月份欄位
    df['year'] = df.index.year
    df['month'] = df.index.month

    # 計算月與年的交叉表
    df_crosstab = pd.crosstab(
        df['month'], df['year'],
        values=df['monthly_return'], aggfunc='mean'  # 以平均數計算每月的報酬率
    )

    # 格式化數字以兩位小數顯示，並替換 NaN 為空字符串
    df_crosstab = df_crosstab.applymap(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

    # 使用matplotlib繪製表格並去除背景顏色
    fig, ax = plt.subplots(figsize=(14, 8))  # Increase figure size for larger table
    ax.axis('off')  # 去掉坐標軸

    # 顯示文字表格
    table = ax.table(cellText=df_crosstab.values,
                    rowLabels=df_crosstab.index,
                    colLabels=df_crosstab.columns,
                    loc='center',
                    cellLoc='center',
                    colColours=['lightgrey'] * len(df_crosstab.columns))

    # 設置字體大小
    table.auto_set_font_size(False)  # 禁用自動設置字體大小
    table.set_fontsize(16)  # 設置字體大小為16（可根據需要調整）

    # 設置格子大小
    for (i, j), cell in table.get_celld().items():
        cell.set_height(0.06)  # 設置行高
        cell.set_width(0.055)   # 設置列寬
        cell.set_fontsize(12)  # 設置格子內文字的字體大小（可根據需要調整）

    # 顯示表格
    plt.title('Monthly Returns per Year', fontsize=18)  # 增加標題字體大小
    plt.show()
