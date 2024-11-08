import time
from datetime import timedelta, datetime
from threading import Thread
from warnings import catch_warnings

from pandas.core.interchange.dataframe_protocol import DataFrame
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import threading
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
from winerror import NOERROR

import requests
from bs4 import BeautifulSoup as bs, BeautifulSoup
from selenium.webdriver.chrome.options import Options

#NAMES
def filter1(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.ID, 'Code')))
    names = driver.find_elements(By.TAG_NAME, 'option')
    names = [str(n.text) for n in names]
    names2=[]
    for n in names:
        if any(char.isdigit() for char in n):
            continue
        else:
            names2.append(n)
    print(len(names2))
    df=pd.DataFrame({
    'Names': names2,
    })
    df.to_csv('stocks/names.csv',index=False)
    filter2(url)

#CHECK 10 YEARS IF EXISTS AND IF NEED UPDATE
def filter2(url):
    df=pd.read_csv('stocks/names.csv')
    names=df.Names
    newNames=[]
    oldNames=[]
    oldDates=[]
    newDates=[]
    for n in names:
        try:
            temp=pd.read_csv(f'stocks/data/{n}.csv')
            if temp is not None:
                date=temp['Date'].iloc[-1]
                oldNames.append(n)
                #TODO Transform date into DateTime
                oldDates.append(date)
        except:
            newNames.append(n)
            newDates.append(datetime(2014, 1, 1))

    #update so threading
    percent=0.25
    arr1=newNames[:int(len(newNames)*percent)]
    arr2=newNames[int(len(newNames)*percent):int(len(newNames)*(percent*2))]
    arr3=newNames[int(len(newNames)*percent*2):int(len(newNames)*(percent*3))]
    arr4=newNames[int(len(newNames)*percent*3):]
    # arr5=newNames[int(len(newNames)*percent*4):]
    darr1 = newDates[:int(len(newDates) * percent)]
    darr2 = newDates[int(len(newDates) * percent):int(len(newDates) * (percent * 2))]
    darr3 = newDates[int(len(newDates) * percent * 2):int(len(newDates) * (percent * 3))]
    darr4 = newDates[int(len(newDates) * percent * 3):int(len(newDates) * (percent * 4))]
    # darr5 = newDates[int(len(newDates) * percent * 4):]
    threads=[]
    threads.append(threading.Thread(target=update, args=(darr1,arr1,url)))
    threads.append(threading.Thread(target=update, args=(darr2,arr2,url)))
    threads.append(threading.Thread(target=update, args=(darr3,arr3,url)))
    threads.append(threading.Thread(target=update, args=(darr4,arr4,url)))
    # threads.append(threading.Thread(target=update, args=(darr5,arr5,url)))
    # update(darr1,arr1,url)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("FINISHED")
    #filter3


#UPDATE TILL TODAY
def filter3(names,dates):

    percent=0.2

    thread=threading.Thread(target=update,args=())
    # Iterate through each name in the DataFrame



    pass



def update(dates,names,url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    date_to = datetime.today()
    for name,date in zip(names,dates):
        interval = timedelta(days=365)
        Input = driver.find_element(By.ID, 'Code')
        Input.send_keys(name)
        # Iterate through the dates in 365-day intervals
        current_date = date
        new_list=[]
        while current_date < date_to:
            end_date=current_date + interval
            if end_date > date_to:
                end_date = date_to

            fromDateInput = driver.find_element(By.ID, 'FromDate')
            fromDateInput.clear()
            fromDateInput.send_keys(current_date.strftime('%d.%m.%Y'))
            toDateInput = driver.find_element(By.ID, 'ToDate')
            toDateInput.clear()
            toDateInput.send_keys(end_date.strftime('%d.%m.%Y'))
            btn = driver.find_element(By.CLASS_NAME, 'btn-primary-sm')
            btn.click()
            # TO DO
            WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
            time.sleep(0.5)
            table = driver.find_element(By.CSS_SELECTOR, '#resultsTable > tbody:nth-child(2)')
            soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
            elements = soup.find_all('tr')
            for i in range(len(elements)):
                tds = elements[-i].find_all('td')
                date = tds[0].text
                last_traded_price = tds[1].text
                max= tds[2].text
                min = tds[3].text
                avg_price = tds[4].text
                promet = tds[5].text
                volume = tds[6].text
                promet_BEST = tds[7].text
                promet_vo_denari = tds[8].text
                stock={
                    "Date":date,
                    "last_traded_price":last_traded_price,
                    "max":max,
                    "min":min,
                    "avg_price":avg_price,
                    "promet":promet,
                    "volume":volume,
                    "promet_BEST":promet_BEST,
                    "promet_vo_denari":promet_vo_denari
                }
                new_list.append(stock)

            current_date = end_date
        df=pd.DataFrame(new_list)
        print(f"FINISHED with {name}")
        df.to_csv(f'stocks/data/{name}.csv',index=False)



url='https://www.mse.mk/mk/stats/symbolhistory/ALK'
filter1(url)
