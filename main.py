import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import telegram
import asyncio
import time

api_key = ''
user_id = ''

MINUTES = 10


def element(driver, xpath):
    return driver.find_elements(by=By.XPATH, value=xpath)[0]


def poll_page():
    driver = webdriver.Firefox()
    try:
        driver.get(
            "https://www.")
        # assert "Python" in driver.title
        elem = element(driver, '//*[@id="plhMain_tbxWebRefNo"]')
        elem.clear()
        elem.send_keys("")
        time.sleep(1)
        elem = element(driver, '//*[@id="plhMain_tbxLastName"]')
        elem.clear()
        elem.send_keys("")
        time.sleep(1)
        elem = element(driver, '//*[@id="plhMain_tbxEmailID"]')
        elem.clear()
        elem.send_keys("s@gmail.com")
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        time.sleep(15)
        elem = element(driver, '//*[@id="plhMain_btnReSch"]')
        elem.send_keys(Keys.RETURN)
        time.sleep(30)
        elem = element(driver,
                       '/html/body/form/div[3]/div[2]/div/div[1]/div/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]')
        month = elem.get_attribute("innerHTML")
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"), month)
        return month
    except Exception as e:
        msg = type(e).__name__
        print(msg)
        return msg
    finally:
        driver.close()


# poll_page()
august_counter = 0


async def send(msg):
    try:
        bot = telegram.Bot(token=api_key)
        global august_counter
        if 'J' in msg or 'j' in msg:
            await bot.send_message(chat_id=user_id, text=msg)
            time.sleep(1)
            await bot.send_message(chat_id=user_id, text="HURRY UP NOW")
        elif 'August' in msg:
            if august_counter % 4 == 0:
                await bot.send_message(chat_id=user_id, text=f'Sorry! {msg}', )
            august_counter += 1
        else:
            await bot.send_message(chat_id=user_id, text=f'what is this {msg}')

    except Exception as e:
        msg = type(e).__name__
        print(msg)


while True:
    try:
        asyncio.run(send(poll_page()))
        time.sleep(60 * MINUTES)
    except Exception as e:
        msg = type(e).__name__
        print(msg)
