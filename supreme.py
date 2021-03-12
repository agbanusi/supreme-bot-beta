import requests
import urllib.parse
import json
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
idea=0
url_json = "https://www.supremenewyork.com/mobile_stock.json"
key = "f8546b398af46006b697645ffbfe01dd"
supreme = "6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz"

usCheckoutData = {
        'store_credit_id': '',
        'from_mobile': '1',
        'same_as_billing_address': '1',
        'order[billing_name]': 'Blah Blah',
        'order[email]': 'blah@gmail.com',
        'order[tel]': '3472002000',
        'order[billing_address]': '1000 Cool Place',
        'order[billing_address_2]': 'Apt 2A',
        'order[billing_zip]': '10101',
        'order[billing_city]': 'NYC',
        'order[billing_state]': 'NY',
        'order[billing_country]': 'USA',
        'credit_card[cnb]': '4128 2000 3000 4000',
        'credit_card[month]': '08',
        'credit_card[year]': '2020',
        'credit_card[rsusr]': '302',
        'order[terms]': '1'
    };

#mobile user-agent header for checkout.json endpoint
headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.supremenewyork.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

def checkoutData(size, amount):
    items={}
    items[size] = 1
    
    print(items)

    cooksub = urllib.parse.quote(json.dumps(items))
    #print(json.dumps(items))
    #print(cooksub)

    usCheckoutData = {
        'store_credit_id': '',
        'from_mobile': '1',
        'cookie-sub': cooksub,
        'same_as_billing_address': '1',
        'order[billing_name]': 'Blah Blah',
        'order[email]': 'blah@gmail.com',
        'order[tel]': '3472002000',
        'order[billing_address]': '1000 Cool Place',
        'order[billing_address_2]': 'Apt 2A',
        'order[billing_zip]': '10101',
        'order[billing_city]': 'NYC',
        'order[billing_state]': 'NY',
        'order[billing_country]': 'USA',
        'credit_card[cnb]': '4128 2000 3000 4000',
        'credit_card[month]': '08',
        'credit_card[year]': '2020',
        'credit_card[rsusr]': '302',
        'order[terms]': '1'
    };
    #,
    #    'g-captcha-response': ''
    return usCheckoutData;

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

# Add the item to your cart
# Needs variant, cw, id
# returns addResp
def addToCart(size, ID):
    session = requests.Session()
    addUrl = "http://www.supremenewyork.com/shop/" + str(ID) + "/add.json"
    
    addPayload = {
        'size': str(size),
        'qty': 1
    }


    addResp = session.post(addUrl, data=addPayload, headers=headers)


    if addResp.status_code != 200:
        print (addResp.status_code)
        
        sys.exit("0001")
    elif addResp.json() == {}:
        print ('Response Empty! - Problem Adding to Cart')
        sys.exit("0003 {}")
    else:
        print (' added to cart!')
        return addResp.json()


def fetchVariants(sizeId, region, amount):
    product_json = "https://www.supremenewyork.com/checkout.json"
    
    #solve the captcha code
    #token = solveCaptcha()
    #datum = addToCart(6, sizeId)
    #print(datum)
    dat = checkoutData(sizeId, amount)
    browse(sizeId, dat)

    #append to checkout info
    #dat['g-recaptcha-response'] = token

    #send data to api
    x = requests.post(product_json, data=dat, headers=headers )
    
    # extracting data in json format 
    data = x.json() 
    print(data)

    variants=[]
    
    if 'status' in data and data['status'] == 'outOfStock':
        for var in data['mp']:
            variants.append({
                    'Product Name': data['mp'][var]['Product Name'],
                    'Product Color': data['mp'][var]['Product Color'],
                    'Product Size': data['mp'][var]['Product Size'],
                    'Product ID': int(sizeId) + int(var)
                })

    return variants

def scrape(search="", cat="", size=""):
    x = requests.get(url_json)

    # extracting data in json format 
    data = x.json() 

    product = data ['products_and_categories']
    items = []
    item = 0

    if len(search)>0:
        product = searched(search, product)
        
    if len(cat) >0:
        item = checked(product, cat, size)
    else:
        #print(product)
        for cat in product:
            items.append(checked(product, cat, size))
        #print(items)
        items = [i for i in items if i>0]
        if len(items)>0:
            rand_no = random.randint(0, len(items)-1)
            item = items[rand_no]
    
    return item

def searched(search, prod):
    result={}
    for cat in prod:
        #print(cat)
        searched = [i for i in prod[cat] if i['name'].find(search) != -1 ]
        #print(searched)
        result[cat] = searched
    
    return result

def checked(product, cat, size):
    largestId=0
    itemId = 0
    for item in product[cat]:
            if len(size)>0:
                sizeId = getExactSizeId(item['id'], size)
            else:
                sizeId = getLargestSizeId(item['id'])
                print(item['id'])
                
                if sizeId > largestId:
                    largestId = sizeId
                    itemId = item['id']
    
    return itemId

def browse(ide, dat):
    link = f"https://www.supremenewyork.com/shop/{ide}"
    driver.get(link)
    
    try:
        driver.find_element_by_name('commit').click()
        time.sleep(0.25)
    except:
        print("Item sold out unfortunately")
        sys.exit("Work Done")

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

        try:
            elem = driver.find_element_by_css_selector('iframe>[id="recaptcha-token"]')
            token = "" #solveCaptcha()
            driver.execute_script('''
                var elem = arguments[0];
                var value = arguments[1];
                elem.value = value;
            ''', elem, token)
        except:
            print("This is as far as I can go please")
        finally:
            sys.exit("Gracias!")
        
        #order_cnb.send_keys(token)


def main():
    region = 'us'
    amount = 1000
    #ide = getLargestItemId(region)
    idd = scrape("Cargo Sweatpant")
    print(idd)
    variants = fetchVariants(idd, region, amount)
    print(variants)

    for i in variants:
        print(i)

if __name__ == '__main__':
    main()