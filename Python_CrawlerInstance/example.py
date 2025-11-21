from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from time import sleep
import os

def open_browser(base_download_dir: str) -> webdriver:
    """啟動 Selenium 瀏覽器，並設定下載路徑"""
    chrome_driver_path = r"C:\your_path\chromedriver.exe"
    # 你下載的chromedriver.exe位置
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.default_directory": base_download_dir
    })

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://tisvcloud.freeway.gov.tw/history/motc20/Section/")

    return driver

def get_data_url(driver: webdriver, base_download_dir: str):
    """取得指定日期範圍的下載連結，並下載資料"""
    # today = datetime.today()
    target_date = datetime.strptime("20250324", "%Y%m%d")
    date_range = [(target_date - timedelta(days=i)).strftime("%Y%m%d") for i in range(30)]
    
    for data in date_range:
        """為特定日期下載 XML.GZ 檔案"""
        date_download_dir = os.path.join(base_download_dir, data)
        os.makedirs(date_download_dir, exist_ok=True)

        driver = open_browser(date_download_dir)
        sleep(5)

        link = driver.find_element(By.XPATH, "//td[@class='indexcolname']/a[contains(@href, '{data}')]".format(data=data))
        print("找到下載連結並且執行")
        link.click()

        sleep(2)
        get_data_gz(driver , date_download_dir)
        driver.quit()

def get_data_gz(driver: webdriver , date_download_dir: str):
    """下載符合條件的 .xml.gz 檔案"""
    wait = WebDriverWait(driver, 60)  # 增加等待時間
    links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='indexcolname']/a[contains(@href, '.xml.gz')]")))
    
    for link in links:
        href = link.get_attribute("href")
        if "LiveTraffic_" in href and ".xml.gz" in href:
            file_number = int(href.split("LiveTraffic_")[1].split(".xml.gz")[0])
            if 1 <= file_number <= 2358:
                filename = f"LiveTraffic_{file_number}.xml.gz"
                filepath = os.path.join(date_download_dir, filename)

                # 檢查檔案是否已存在
                if os.path.exists(filepath):
                    print(f"檔案已存在，跳過下載: {filename}")
                    continue
                
                print(f"下載檔案: {href}")
                link.click()
                sleep(1)

if __name__ == "__main__":
    base_download_dir = r"C:\Users\your_path\Downloads"
    # 下載的路徑

    driver = open_browser(base_download_dir)
    sleep(5)
    get_data_url(driver, base_download_dir)

    driver.quit()
