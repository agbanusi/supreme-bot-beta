import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from harvester import browser, fetch

def capture():
    ReCaptchaV2(
    url='supremenewyork.com',
    sitekey="6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz"
)

def ReCaptchaV2(url, sitekey):
    #print(url, sitekey)
    os.system(f"harvester recaptcha-v2 -d {url} -k {sitekey} -b chrome")
    tokens()

def tokens():
    token = fetch.token("supremenewyork.com")
    # Write-Overwrites
    print(token)
    file1 = open("tokens.txt","w")#write mode
    file1.write(f"{token} \n")
    file1.close()
    return token

if __name__ == '__main__':
    capture()