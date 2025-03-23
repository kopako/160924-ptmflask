#!/usr/bin/env python3
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    web_driver = webdriver.Chrome()

    web_driver.get("https://itcareerhub.de")
    web_driver.fullscreen_window()

    accept_cookies_button = web_driver.find_element(By.XPATH, '//button[text()="Bestätigen"]')
    accept_cookies_button.click()
    WebDriverWait(web_driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//a[text()="Zahlungsarten"]'))
                )
    payment_link = web_driver.find_element(By.XPATH, '//a[text()="Zahlungsarten"]')
    payment_link.click()
    current_dir = os.getcwd()
    screenshot_status = web_driver.save_screenshot(os.path.join(current_dir, "screenshot_payment.png"))
    print("screenshot successfull") if screenshot_status else print("SCREENSHOT FAILED")
finally:
    web_driver.quit()