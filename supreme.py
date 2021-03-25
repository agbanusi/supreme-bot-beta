import requests
import urllib.parse
import json
import time
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from harvester import browser, fetch
#import subprocess
from multiprocessing import Process

def getLargestItemId(region):
    x = requests.get(url_json)

    # extracting data in json format 
    data = x.json() 

    product = data ['products_and_categories']
    largestId = 0

    if region == 'us' and 'new' in product:
        largestId = max([p['id'] for p in product['new']])
        largestId = getLargestSizeId(largestId)
    else:
        for cat in product:
            for item in product[cat]:
                sizeId = getLargestSizeId(item['id'])
                if sizeId > largestId:
                    largestId = sizeId

    return largestId

def getLargestSizeId(ide):
    #print(id)
    product_json = f"https://www.supremenewyork.com/shop/{ide}.json"
    x = requests.get(product_json)
    
    # extracting data in json format 
    data = x.json()
    
    lastProduct = data['styles'][len(data['styles']) - 1]
    lastProductID = lastProduct['sizes'][len(lastProduct['sizes'])- 1]['id']
    
    return lastProductID

def getExactSizeId(ide, size):
    #print(id)
    product_json = f"https://www.supremenewyork.com/shop/{ide}.json"
    x = requests.get(product_json)
    
    # extracting data in json format 
    data = x.json()
    #print(data)
    lastProduct = data['styles'][len(data['styles']) - 1]
    ProductID = [i for i in lastProduct['sizes'] if i['name'] == size] [0]['id']
    
    return ProductID

def solveCaptcha():
    product = "https://www.supremenewyork.com/checkout.json"
    url = "http://2captcha.com/in.php?key="+key+"&json=1&method=userrecaptcha&googlekey="+supreme+"&pageurl="+product+""

    x=requests.get(url)
    data = x.json()
    token = None
    if data['status'] == 1:
        t = 0
        while t==0:
            time.sleep(5)
            y = requests.get("http://2captcha.com/res.php?json=1&key="+key+"&action=get&id="+data['request'])
            datum = y.json()
            if datum['status'] == 1:
                token = datum['request']
                t=1
    
    return token

def scrape(search="", cat="", size=""):
    x = requests.get(url_json)

    # extracting data in json format 
    data = x.json() 

    product = data ['products_and_categories']
    items = []
    ids = []
    item = 0
    idd = 0
    #print(product)
    if len(search)>0:
        product = searched(search, product)
        
    if len(cat) >0:
        item, sizeId = checked(product, cat, size)
        idd = sizeId
    else:
        #print(product)
        for cat in product:
            ide, sizeIds = checked(product, cat, size)
            items.append(ide)
            ids.append(sizeIds)
        #print(items)
        #print(ids)

        ids = [ids[i] for i in range(len(ids)) if items[i] > 0]
        items = [i for i in items if i>0]

        if len(items)>0:
            rand_no = random.randint(0, len(items)-1)
            item = items[rand_no]
            idd = ids[rand_no]
    
    return item, idd

def searched(search, prod):
    result={}
    for cat in prod:
        #print(cat)
        searched = [i for i in prod[cat] if i['name'].lower().strip().find(search.lower().strip()) != -1 ]
        #print(searched)
        result[cat] = searched
    
    return result

def checked(product, cat, size):
    largestId=0
    itemId = 0
    sizeId = 0
    for item in product[cat]:
            if len(size)>0:
                sizeId = getExactSizeId(item['id'], size)
            else:
                sizeId = getLargestSizeId(item['id'])
                #print(item['id'])
                
                if sizeId > largestId:
                    largestId = sizeId
                    itemId = item['id']
    
    return (itemId, sizeId)

def browse(ide, sizeId):
    link = f"https://www.supremenewyork.com/shop/{ide}"
    usCheckoutData = card_details()
    driver.get(link)
    
    try:
        driver.find_element_by_name('commit').click()
        time.sleep(0.25)
    except:
        print( "Item sold out unfortunately for item "+str(ide) )
        return 
        #sys.exit("Work Done")

    driver.get("https://www.supremenewyork.com/checkout")
    
    #order_bill_name = driver.find_element_by_xpath("//input[@id='']")
    
    try:
        driver.find_element_by_css_selector('[id="order_billing_name"]')
    
    except:
        time.sleep(0.5)
        driver.get("https://www.supremenewyork.com/checkout")

    finally:
        order_bill_name = driver.find_element_by_xpath("//input[@id='order_billing_name']")
        order_bill_name.send_keys(usCheckoutData['order[billing_name]'])
        time.sleep(0.25)
        order_email = driver.find_element_by_xpath("//input[@id='order_email']")
        order_email.send_keys(usCheckoutData['order[email]'])
        time.sleep(0.25)
        order_tele = driver.find_element_by_xpath("//input[@id='order_tel']")
        order_tele.send_keys(usCheckoutData['order[tel]'])
        time.sleep(0.25)
        order_address = driver.find_element_by_xpath("//input[@id='bo']")
        order_address.send_keys(usCheckoutData['order[billing_address]'])
        time.sleep(0.35)
        #order_bill_city = driver.find_element_by_xpath("//input[@id='order_billing_city']")
        #order_bill_city.send_keys("Testingburg")
        order_bill_zip = driver.find_element_by_xpath("//input[@id='order_billing_zip']")
        order_bill_zip.send_keys(usCheckoutData['order[billing_zip]'])
        time.sleep(0.25)
        order_cnb = driver.find_element_by_xpath("//input[@id='rnsnckrn']")
        order_cnb.send_keys(usCheckoutData['credit_card[cnb]'])
        time.sleep(0.5)
        order_cnb = driver.find_element_by_xpath("//input[@id='orcer']")
        order_cnb.send_keys(usCheckoutData['credit_card[rsusr]'])
        time.sleep(0.25)
        order_cnb = driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins')
        order_cnb.click()
        time.sleep(0.25)
        Select(driver.find_element_by_xpath('//*[@id="credit_card_month"]')).select_by_visible_text(usCheckoutData['credit_card[month]'])
        time.sleep(0.25)
        Select(driver.find_element_by_xpath('//*[@id="credit_card_year"]')).select_by_visible_text(usCheckoutData['credit_card[year]'])
        time.sleep(0.255)
        driver.find_element_by_name('commit').click()

        #try:
            #elem = driver.find_element_by_id('g-recaptcha-response')
        token = getToken() #solveCaptcha()
        print(token)
        #driver.execute_script('document.getElementById("recaptcha-token").value = "%s"'
        #% token)
        order_cnb = driver.find_element_by_xpath("//*[@id='recaptcha-token']")
        order_cnb.send_keys(token)
        '''except:
            print("This is as far as I can go please")
        finally:
            #driver.quit()
            #sys.exit("Gracias!")
            print("done")
            return'''
        #order_cnb.send_keys(token)

def words():
    lines = []
    with open("items.txt") as f:
        lines = f.readlines()
    
    return lines

def card_details():
    lines = []
    card = {}
    with open("card.txt") as f:
        lines = f.readlines()
    
    for i in lines:
        name = i.split("=")[0].replace("\n","").strip()
        value = i.split("=")[1].replace("\n","").strip()
        
        if(name == "billing_name"):
            card["order[billing_name]"] = value
        elif (name =="email"):
            card["order[email]"] = value
        elif name == "tel":
            card["order[tel]"] = value
        elif name == "billing_address":
            card["order[billing_address]"] = value
        elif name == "billing_zip":
            card["order[billing_zip]"] = value
        elif name == "billing_city":
            card["order[billing_city]"] = value
        elif name == "billing_state":
            card["order[billing_state]"] = value
        elif name == "billing_country":
            card["order[billing_country]"] = value
        elif name == "card_number":
            card["credit_card[cnb]"] = value
        elif name == "month":
            card["credit_card[month]"] = value
        elif name == "year":
            card["credit_card[year]"] = value
        elif name == "cvv":
            card["credit_card[rsusr]"] = value
        else:
            print("Not found")
            sys.exit("Fatal Error , need complete credit data")
            driver.quit()
    return card

def harvestOne():
    # check to see if any profiles exist already
    if not browser.get_profiles():
        # create a new profile
        profile = browser.new_profile('Footeam')
        # this will open a window which allows the user to login to google
        # it will block until the user close the browser, browser, not the window
        profile.login_to_google()
    else:
        # load the profile that should exist after running the code a second time
        profile = browser.get_profile('Footeam')

    # this will create a window which will connect to the server
    # and display captcha's to the user when they are requested
    # later in in the code
    profile.harvest()

def harvestMultiple(num):
    # check to see if any profiles exist already
    existing_profiles = len(browser.get_profiles())
    if existing_profiles < num:
        for i in range(existing_profiles - num):
            profile = browser.new_profile(f'Footeam-{i}')
            profile.login_to_google()

    for profile in browser.get_profiles():
        profile.harvest()

def getToken():
    #intercepter = harvester.capture(captcha)
    #token = intercepter.tokens.get()
    file1 = open("tokens.txt","r")
    fin = file1.readline()
    file1.close()
    return fin

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

def main():
    #region = 'us'
    #amount = 1000
    #ide = getLargestItemId(region)
    #harvestOne()
    items = words()
    #print(items)
    for i in range(len(items)):
        if i>0:
            it = items[i].replace("\n","").strip()
            item = it.split("/")
            item = [i.strip() for i in item]
            if i > 1:
                driver.execute_script('''window.open("https://www.supremenewyork.com","_blank");''')
                driver.switch_to.window(driver.window_handles[i-1])
            if len(item) == 1:
                idd, sizeId = scrape(item[0])
            elif len(item) == 2:
                idd, sizeId = scrape(item[0], item[1])
            elif len(item) == 3:
                idd, sizeId = scrape(item[0], item[1], item[2])
            else:
                sys.exit("Error Occured, check items.txt and try again")
            browse(idd, sizeId)
        #print(idd, sizeId)
    
    #print(variants)
def capture():
    ReCaptchaV2(
    url='supremenewyork.com',
    sitekey=supreme
)

## Global variables
driver = webdriver.Chrome()
url_json = "https://www.supremenewyork.com/mobile_stock.json"
key = "f8546b398af46006b697645ffbfe01dd"
supreme = "6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz"

#harvester = Harvester().serveforever()
#intercepter = harvester.capture(captcha)
#browser = intercepter.setup_browser(user_data_dir='ChromeData')

if __name__ == '__main__':
    #main()
    p1 = Process(target=capture)
    p1.start()
    p2 = Process(target=main)
    p2.start()
    p1.join()
    p2.join()