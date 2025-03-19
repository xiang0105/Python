import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

def YearlyReturnBarChart():
    # 讀取加權投資組合資料
    df = pd.read_csv(r'csv\weighted_portfolio.csv')

    # 確保日期格式正確
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # 確保 'Close' 欄位是數字型
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # 計算每日收益率
    df['daily_return'] = df['Close'].pct_change()

    # 新增年份和月份欄位
    df['year'] = df.index.year
    df['month'] = df.index.month

    # 1. 計算年報酬率並繪圖
    df_yearly_return = df.groupby('year')['daily_return'].sum()

    # 使用 matplotlib 的 bar 方法繪製條形圖
    fig, ax = plt.subplots(figsize=(15, 5))
    bars = ax.bar(
        df_yearly_return.index, df_yearly_return.values,
        color='skyblue', label="Yearly Returns"
    )
    ax.set_title("Portfolio Yearly Performance")
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual Return")
    ax.grid(True)

    # 添加滑鼠懸停功能
    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect(
        "add", 
        lambda sel: sel.annotation.set_text(
            f"Year: {int(sel.target[0])}\nReturn: {sel.target[1]:.2%}"
        )
    )

    plt.show()

    # 2. 計算月與年的交叉表
    df_crosstab = pd.crosstab(
        df['month'], df['year'],
        values=df['daily_return'], aggfunc='sum'
    )

    # 格式化為百分比
    df_crosstab = df_crosstab.applymap(lambda x: f"{x:.2%}" if pd.notnull(x) else "N/A")

    # 顯示交叉表
    print(df_crosstab)

    # 保存交叉表為 CSV 文件
    df_crosstab.to_csv(r'csv\year_month_return_crosstab.csv')
