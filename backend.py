import requests
from bs4 import BeautifulSoup

import streamlit as st
import pandas as pd
import IPython
from IPython.core.display import HTML, display
from time import sleep
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC



from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
option = Options()
option.add_argument('--headless')
# Creating Front end using StreamLit

st.title("E-commerce website Data Extraction")

st.write("See all the products of websites like Amazon, Flipkart in one click")

platform=st.selectbox('Choose Platform',['','Flipkart','Amazon'])

product_name = st.text_input("Enter Product Name")

button = st.button("Submit")

def flipkart():
    url = f"https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    res = requests.get(url)
    #print(res.status_code)
    soup = BeautifulSoup(res.content,'html.parser')
    prod_list = []
    prod_name = soup.find_all('div', class_='_4rR01T')
    for i in prod_name:
        prod_list.append(i.text.strip())

    #Features
    feature_list = []
    features = soup.find_all('ul', class_='_1xgFaf')
    for i in features:
        feature_list.append(i.text.strip())

    #feature_list

    # Prices
    price_list = []
    prices = soup.find_all('div','_30jeq3 _1_WHN1')
    for i in prices:
        price_list.append(i.text.strip())
    
    #price_list

    # Rating
    rating_list = []
    ratings = soup.find_all('div', class_ = '_3LWZlK')
    for i in ratings:
        rating_list.append(i.text.strip())
    #rating_list

    # images
    links=[]
    images = soup.find_all('div',class_='CXW8mj')
    for image in images:
        img_tag = image.find('img')
        img_src = img_tag['src']
        links.append(img_src)
    items = {'Product Name':prod_list[:20], 'Features':feature_list[:20],'Rating':rating_list[:20],'Price':price_list[:20]}
    
    return items, links

def amazon():
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
    
    driver.get("https://www.amazon.in")
    sleep(10)
    input_search = driver.find_element(By.ID,"twotabsearchtextbox")#a-size-medium a-color-base a-text-normal
    input_search.send_keys(product_name)
    search_but = driver.find_element(By.ID, 'nav-search-submit-button')
    search_but.click()
    sleep(10)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    container = soup.select('.s-card-container')
    
    name_list = []
    prices = []
    links = []
    for i in container:
        #class="a-size-base puis-bold-weight-text"
        name = i.find('span','a-size-medium a-color-base a-text-normal')
        price = i.find('span','a-price-whole')
        #rating = i.find('span',{'class':'a-size-base puis-bold-weight-text'})
        imgs = i.find('div',"a-section aok-relative s-image-fixed-height")
        name_list.append(name)
        prices.append(price)
        links.append(imgs)

    def remove_none(lst):
        lsts = []
        for i in lst:
            if i is None:
                continue
            else:
                lsts.append(i.text.strip())
            
        return lsts
    prod_names = remove_none(name_list)
    prices_list = remove_none(prices)
    #ratings_list = remove_none(ratings)
    #for i in ratings:
    links_list = []
    for i in links:
        if i is None:
            continue
        else:
            img_tag = i.find('img')
            img_src = img_tag['src']
            links_list.append(img_src)

    return prod_names, prices_list, links_list

if button:
    if platform=="Flipkart":
        items, links = flipkart()
        df = pd.DataFrame(items)
        df['Product_Image'] = links[:20]
        def to_img_tag(path):
            return '<img src="'+ path + '" width="100" >'
        st.write(HTML(df.to_html(escape=False,formatters=dict(Product_Image=to_img_tag))))
    elif platform=='Amazon':
        l1,l2,l3 = amazon()
        
        items = {'Product Name':l1[:15],'Price':l2[:15]}
        
        #items = {'Product Name':prod_names,'Price':prices_list[:mini]}
        df = pd.DataFrame(items)
        df['Product_Image'] = l3[:15]
        def to_img_tag(path):
            return '<img src="'+path+'" width="100">'
        st.write(HTML(df.to_html(escape=False, formatters=dict(Product_Image=to_img_tag))))
        
        
        
    

