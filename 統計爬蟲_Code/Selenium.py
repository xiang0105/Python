from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import json

def open_browser() -> webdriver:
    chrome_driver_path = r"C:\Users\56433\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.10\chromedriver.exe"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(r"user-data-dir=C:\Users\56433\AppData\Local\Google\Chrome\User Data")
    options.add_argument("profile-directory=Profile 1")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.x.com/home")

    return driver

def get_data(post) -> dict:

    sleep(5)
    
    data = {
        "Time": get_data_time(post),
        "Name": get_data_name(post),
        "Content": get_data_content(post),
        "Views": get_data_view(post),
        "Likes": get_data_like(post)
    }
    data_list.append(data)

def get_data_time(post) -> str:

    time_element = post.find_element(By.XPATH, ".//time")
    datetime_value = time_element.get_attribute("datetime")

    return datetime_value

def get_data_name(post) -> str:

    name_element = post.find_element(By.XPATH, ".//span[contains(@class, 'css')][1]")
    return name_element.text

def get_data_content(post) -> str:

    content_element = post.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
    return content_element.text

def get_data_view(post) -> str:

    view_link = post.find_element(By.XPATH, ".//a[contains(@aria-label,'View')]")    
    view_count = view_link.find_element(By.XPATH, ".//span[contains(@class, 'css-1jxf684')]")
        
    return view_count.text

def get_data_like(post) -> str:

    like_button = post.find_element(By.XPATH, ".//button[contains(@aria-label, 'Like')]")
    like_count = like_button.find_element(By.XPATH, ".//span[contains(@class, 'css-1jxf684')]")
    
    return like_count.text
    
data_list = []

if __name__ == "__main__":

    driver = open_browser()

    for _ in range(2):  
        try:
            posts = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']") 
            for post in posts:
                if post not in data_list:
                    try:
                        get_data(post)
                    except StaleElementReferenceException:
                        print("⚠️ 元素已變更，重新嘗試抓取...")
                        continue 
        except Exception as e:
            print(f"⚠️ 發生錯誤: {e}")

        for _ in range(5):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            sleep(2) 

    with open('data.json','w',encoding = 'utf-8') as f :
        json.dump(data_list,f, indent=2, sort_keys=True, ensure_ascii=False)

    input("Press Enter to close the browser...")