import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from python_code import Grab_Stocks
from python_code import Draw_Charts
from python_code import Analyze_Stocks

class ETFAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETF Stock Analyzer")
        self.root.geometry("600x500")  # 可以增大視窗來顯示圖表

        # 標題
        self.title_label = tk.Label(self.root, text="ETF Stock Analyzer", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # 輸入ETF名稱
        self.ticker_label = tk.Label(self.root, text="Enter ETF Tickers (comma-separated):")
        self.ticker_label.pack(pady=5)
        self.ticker_entry = tk.Entry(self.root, width=40)
        self.ticker_entry.insert(0, "SPY, QQQ, VTI")  # 預設值
        self.ticker_entry.pack(pady=5)

        # 起始日期
        self.start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = tk.Entry(self.root, width=40)
        self.start_date_entry.insert(0, "2023-01-01")  # 預設值
        self.start_date_entry.pack(pady=5)

        # 終止日期
        self.end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD):")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = tk.Entry(self.root, width=40)
        self.end_date_entry.insert(0, "2023-12-31")  # 預設值
        self.end_date_entry.pack(pady=5)

        # 按鈕：執行查詢並繪製圖表
        self.draw_button = tk.Button(self.root, text="Fetch and Draw All ETF Charts", command=self.fetch_and_draw_charts)
        self.draw_button.pack(pady=10)

        # 按鈕：選擇ETF進行分析
        self.analyze_button = tk.Button(self.root, text="Analyze Selected ETF", command=self.analyze_selected_etf)
        self.analyze_button.pack(pady=10)

        # 選擇分析的ETF
        self.selected_ticker_label = tk.Label(self.root, text="Select ETF for Analysis:")
        self.selected_ticker_label.pack(pady=5)
        self.selected_ticker_combo = ttk.Combobox(self.root, values=["SPY", "QQQ", "VTI"], width=37)
        self.selected_ticker_combo.pack(pady=5)

        # # 用來顯示圖表的框架
        # self.chart_frame = tk.Frame(self.root)
        # self.chart_frame.pack(pady=20)

    def fetch_and_draw_charts(self):
        # 讀取用戶輸入的ETF名稱、日期範圍
        tickers = self.ticker_entry.get().split(',')
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # 遍歷每個ETF，抓取資料並儲存
        for ticker in tickers:
            ticker = ticker.strip()  # 去除空格
            try:
                # 呼叫Grab_Stocks抓取資料
                stock_data = Grab_Stocks.GrabStockData(ticker, start_date, end_date)
                Grab_Stocks.SaveToCsv(stock_data, f"./csv/{ticker}_data.csv")
            except Exception as e:
                messagebox.showerror("Error", f"Error fetching data for {ticker}: {e}")
                return
        
        # 顯示所有圖表
        try:
            # 呼叫你的繪圖函數來顯示圖表並返回fig
            fig = Draw_Charts.DrawChart(tickers)  # 繪製圖表並返回fig
            print(fig)
            self.show_chart(fig)
            messagebox.showinfo("Success", "Charts drawn successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error drawing charts: {e}")

    def analyze_selected_etf(self):
        # 取得選擇的ETF進行分析
        selected_ticker = self.selected_ticker_combo.get()
        if selected_ticker:
            try:
                fig = Analyze_Stocks.AnalyzeStoks(selected_ticker)  # 呼叫你的分析函數，並返回fig
                self.show_chart(fig)
                messagebox.showinfo("Success", f"Analysis for {selected_ticker} completed!")
            except Exception as e:
                messagebox.showerror("Error", f"Error analyzing {selected_ticker}: {e}")
        else:
            messagebox.showwarning("Input Error", "Please select an ETF for analysis.")

    def show_chart(self, fig):
        # 在 Tkinter 中顯示圖表
        for widget in self.chart_frame.winfo_children():
            widget.destroy()  # 清除舊的圖表

        # 創建畫布並顯示圖表
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    # 創建Tkinter視窗
    root = tk.Tk()
    app = ETFAnalyzerApp(root)
    root.mainloop()
