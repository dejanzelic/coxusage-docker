from selenium import webdriver
import json
import datetime
import calendar
import os
import time

now = datetime.datetime.now()

cox_user = os.getenv('COX_USER')
cox_pass = os.environ.get('COX_PASSWORD')
json_file_location = os.getenv('JSON_LOCATION').strip()
json_file = f"{json_file_location}"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
print("[+] Starting Chrome")
driver = webdriver.Chrome(options=chrome_options)
print("[+] Getting Login page")
driver.get('https://www.cox.com/content/dam/cox/okta/signin.html')
print("[+] Waiting for fields to load")
time.sleep(5)

username = driver.find_element_by_id("okta-signin-username")
password = driver.find_element_by_id("okta-signin-password")

username.send_keys(cox_user)
password.send_keys(cox_pass)
print("[+] Submitting Login")
driver.find_element_by_id("okta-signin-submit").click()
print("[+] Waiting for login to complete")
time.sleep(5)
print("[+] Loading Usage")
driver.get('https://www.cox.com/internet/mydatausage.cox')

time.sleep(5)
print("[+] Extracting Json")

data = driver.execute_script("return utag_data;")

data["currentMonthDays"] = calendar.monthrange(now.year, now.month)[1]
print("[+] Saving File")

with open(json_file, 'w+') as outfile:
    json.dump(data, outfile, sort_keys=True)
