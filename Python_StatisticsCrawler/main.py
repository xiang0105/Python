from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep

def open_browser() -> webdriver:
    # ChromeDriver 的路徑
    chrome_driver_path = r"chromedriver.exe"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 你要使用的 Chrome 用戶資料夾路徑
    options.add_argument(r"User Data")
    # 這裡的 Profile 1 是 Chrome 的用戶資料夾名稱，根據你的實際情況修改
    options.add_argument("profile-directory=Profile 1")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 啟用無頭模式（隱藏視窗）
    options.add_argument("--headless=new")  # 使用新的無頭模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 渲染（無頭模式下建議）
    options.add_argument("--window-size=1920,1080")  # 設定視窗大小，模擬真實瀏覽器

    # 禁用 WebRTC，防止暴露真實 IP
    options.add_argument("--disable-webrtc")

    # 增加穩定性
    options.add_argument("--no-sandbox")  # 避免某些環境下的權限問題
    options.add_argument("--disable-dev-shm-usage")  # 避免共享內存不足的問題

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # 隱藏 Selenium 自動化標誌
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })

    driver.get("https://www.x.com/home")

    return driver

def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(10)

if __name__ == "__main__":
    driver = open_browser()
    data_list = []

    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data_list = list(reader)  # 將現有的資料讀入 data_list
    except FileNotFoundError:
        pass

    sleep(3)  # 等待頁面加載完成

    for _ in range(5):  # 滾動次數
        articles = driver.find_elements(By.XPATH, "//article")
        for article in articles:
            
            lines = article.text.split("\n")
            # 等待 @name 出現
            name = WebDriverWait(article, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), '@')]"))
            ).text

            # 等待 tweetText 出現
            try:
                content = WebDriverWait(article, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='tweetText']"))
                ).text
            except Exception as e:
                content = "No content found"

            # 等待時間
            try:
                time_posted = WebDriverWait(article, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//time"))
                ).get_attribute("datetime")
            except Exception as e:
                time_posted = "No time found"

            message = lines[-4]
            likes = lines[-2]
            views = lines[-1]

            data = {
                "Name": name,
                "Content": content,
                "Time": time_posted,
                "Number of Message": message,
                "Views": views,
                "Likes": likes
            }

            data_list.append(data)

        scroll()

    with open('data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Content", "Time", "Number of Message", "Views", "Likes"])
        writer.writeheader()  # 寫入表頭
        writer.writerows(data_list)  # 寫入資料

    input("Press Enter to close the browser...")