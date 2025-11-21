from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time
import os
import glob

def open_browser(download_dir: str) -> webdriver.Chrome:
    """開啟瀏覽器並設定下載路徑"""
    chrome_driver_path = r"C:\Users\56433\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.10\chromedriver.exe"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.default_directory": download_dir
    })

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://codis.cwa.gov.tw/StationData")

    return driver

def click_data_interface(driver):
    """點擊進入測站清單與資料畫面"""
    wait = WebDriverWait(driver, 10)

    # 點擊「測站清單」按鈕
    station_list_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '測站清單')]")))
    station_list_btn.click()

    time.sleep(1)  # 加入小等待避免動畫影響

    # 點擊進入資料查詢介面
    # 等待找到 chart_icon 元素
    chart_icons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "i.fa-chart-line.cursor-pointer")))

    second_chart_icon = chart_icons[1]
    parent_div = second_chart_icon.find_element(By.XPATH, "./..")
    
    # 使用 JavaScript 點擊該父元素
    driver.execute_script("arguments[0].click();", parent_div)

    
    time.sleep(5)  # 加入小等待避免動畫影響


def get_data(driver, base_dir, start_date: str, station_names: list, days: int):
    wait = WebDriverWait(driver, 10)
    start = datetime.strptime(start_date, "%Y-%m-%d")

    # 對照地名與代碼（option 的 value）
    station_map = {
        "基隆": "466940", "台北": "466920", "新屋": "467050", "新竹": "467571",
        "後龍": "467280", "台中": "467490", "田中": "467270", "古坑": "467290",
        "嘉義": "467480", "台南": "467410", "高雄": "467441"
    }

    for i in range(days):
        target_date = start - timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")

        day_dir = os.path.join(base_dir, date_str)
        os.makedirs(day_dir, exist_ok=True)

        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": day_dir
        })

        # 日期設定
        date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.datetime-selector")))

        # 點擊以觸發 UI 展開（保險做法）
        driver.execute_script("arguments[0].click();", date_input)

        # 直接用 JS 設定值，不用 send_keys()
        driver.execute_script("arguments[0].value = arguments[1];", date_input, date_str)

        time.sleep(1)

        for name in station_names:
            try:
                # 根據測站名稱取得代碼
                code = station_map.get(name)
                if not code:
                    print(f"❌ 未知測站：{name}")
                    continue

                # 等待 select 元素出現
                station_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.lightbox-tool-stn-select select"))
                )

                # 使用 JavaScript 設定 select 的值
                driver.execute_script("arguments[0].value = arguments[1];", station_select, code)

                # 模擬 change 事件
                driver.execute_script("""
                    const event = new Event('change', { bubbles: true });
                    arguments[0].dispatchEvent(event);
                """, station_select)

                print("✅ 測站代碼已強行附值為：", code)

                # 等待CSV下載按鈕可點擊
                download_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//div[contains(@class, 'lightbox-tool-type-ctrl-btn') and contains(., 'CSV下載')]"
                )))
                download_btn.click()
                print(f"✅ {date_str} - {name} 資料下載到 {day_dir}")

                # 等待下載完成
                wait_for_download_complete(day_dir)

            except Exception as e:
                print(f"⚠️ {date_str} - {name} 發生錯誤：{e}")





def wait_for_download_complete(folder_path, timeout=30):
    """等待下載完成（.crdownload 檔案消失）"""
    end_time = time.time() + timeout
    while time.time() < end_time:
        downloading = glob.glob(os.path.join(folder_path, "*.crdownload"))
        if not downloading:
            return
        time.sleep(1)
    print("⚠️ 等待下載超時，可能尚未完成")


if __name__ == "__main__":
    download_dir = r"C:\Users\56433\OneDrive\桌面\NTUT Data\!公路局路段即時路況動態資訊(v2.0)\降雨量"
    os.makedirs(download_dir, exist_ok=True)

    # 起始日期、測站與天數
    date = "2025-04-14"
    weather_station = ["基隆", "台北", "新屋", "新竹", "後龍", "台中", "田中", "古坑", "嘉義", "台南", "高雄"]
    date_range = 30

    driver = open_browser(download_dir)
    try:
        click_data_interface(driver)
        get_data(driver, download_dir, date, weather_station, date_range)
    finally:
        driver.quit()
