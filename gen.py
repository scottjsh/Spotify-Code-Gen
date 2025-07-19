import os
import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from colorama import Fore

try:
    import undetected_chromedriver as uc
except ModuleNotFoundError:
    os.system('pip install undetected-chromedriver')
    import undetected_chromedriver as uc


def create_hm_account(username, email, password, firstname):
    options = uc.ChromeOptions()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    driver = uc.Chrome(options=options, service_log_path=os.devnull)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 100)

    print(Fore.LIGHTMAGENTA_EX + "Opening Browser..")

    driver.get("https://www2.hm.com/ko_kr/register")

    while True:
        try:
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "dateOfBirth-D").send_keys("1")
            driver.find_element(By.ID, "dateOfBirth-M").send_keys("1")
            driver.find_element(By.ID, "dateOfBirth-Y").send_keys("2000")
            driver.find_element(By.ID, "termsConditions").click()
            driver.find_element(By.ID, "hmCollectionStorage").click()
            driver.find_element(By.ID, "overseasTransfer").click()
            time.sleep(0.8)
            driver.find_element(
                By.XPATH, '//*[@id="__next"]/main/div/form/button[10]').click()
            break
        except Exception:
            pass

        try:
            driver.find_element(By.ID, "name").send_keys(firstname)
            break
        except Exception:
            pass

    time.sleep(1)
    print("Account created! Trying to get spotify code...")

    try:
        # Spotify 코드 가져오기
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/main/div/ul/li[2]/button/article/div[1]/span/img'))).click()
        time.sleep(1)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[4]/div/a'))).click()
        offer_code_element = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[3]/label')))
        offer_code = "https://www.spotify.com/kr-ko/ppt/hm/?code=" + \
            offer_code_element.text.replace("할인 코드 ", "")
        print(f"Offer : {offer_code}")

        # 코드를 파일에 저장
        with open("codes.txt", "a") as file:
            file.write(offer_code + "\n")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


number_of_codes_to_collect = 10

for _ in range(number_of_codes_to_collect):
    username = f"a{''.join(random.sample(string.ascii_lowercase + string.digits, 15))}"
    firstname = f"A{''.join(random.sample(string.ascii_lowercase + string.digits, 14))}"
    lastname = f"L{''.join(random.sample(string.ascii_lowercase + string.digits, 14))}"
    password = f"A{''.join(random.sample(string.ascii_lowercase + string.digits, 15))}&*"
    email = f"{firstname}.{lastname}@example.com"

    print(Fore.LIGHTMAGENTA_EX +
          f"Spotify Gen | ID: {username} PW: {password} E-Mail: {email}")
    create_hm_account(username, email, password, firstname)
    time.sleep(5)
