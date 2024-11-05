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
def filter1(driver):
    names = driver.find_elements(By.TAG_NAME, 'option')
    names = [str(n.text) for n in names]
    dates=[]
    names2=[]
    for n in names:
        if any(char.isdigit() for char in n):
            continue
        else:
            names2.append(n)
            dates.append(None)
    directory_path = Path(f"stocks/files")
    directory_path.mkdir(parents=True, exist_ok=True)

    print(len(names2))
    print(len(dates))
    df=pd.DataFrame({
    'Names': names2,
    'Last_date': dates
    })
    df.to_csv('stocks/names.csv',index=False)

#CHECK 10 YEARS IF EXISTS AND IF NEED UPDATE
def filter2():
    df=pd.read_csv('stocks/names.csv')
    names=df.Names
    i=0
    for n in names:
        try:
            temp=pd.read_csv(f'stocks/data/{n}.csv')
            df.iat[0,1]=temp.Date[-1]
        except:
            print(2)
            df.iat[0, 1]=None

    df.to_csv('stocks/names.csv', index=False)

    pass

#UPDATE TILL TODAY
def filter3(url):
    df = pd.read_csv('stocks/names.csv')
    driver = webdriver.Chrome()
    driver.get(url)
    succ=0
    fail=0
    # Iterate through each name in the DataFrame
    for n in df.Names:

        Input = driver.find_element(By.ID, 'Code')
        # Input.clear()  # Clear previous input
        Input.send_keys(n)
        btn = driver.find_element(By.CLASS_NAME, 'btn-primary-sm')
        btn.click()



        table = driver.find_element(By.ID, 'results')  # Adjust this locator to match your table
        # ActionChains(driver).move_to_element(table).click().perform()

        # time.sleep(200)

        # Wait for the table rows to load after clicking the button
        try:
            # Wait until the expected table rows are present
            WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

            # Re-fetch the elements after waiting
            elements = table.find_elements(By.TAG_NAME, 'tr')[2:] # Skip header rows
            # Iterate through the rows and extract cell text
            for e in elements:
                temp=e.get_attribute('innerHTML')
                soup=bs(temp, 'html.parser')
                date=soup.find('td')
                # Re-fetch cells for the current row
                # print(date.text)
                # cells = e.find_elements(By.TAG_NAME, 'td')
                # if cells:  # Ensure there are cells to avoid index errors
                #     print(cells[0].text)
            succ+=1
            print(f'Succesfully {n}')
        except Exception as e:
            print(f"An error occurred while processing {n}:")
            fail+=1
        time.sleep(0.5)
    print(succ)
    print(fail)


    pass



def update(url, date_from, date_to,name,index):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)


    interval = timedelta(days=365)

    # Iterate through the dates in 365-day intervals
    current_date = date_from
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
        print(f'finished {current_date}')
    df=pd.DataFrame(new_list)
    df.to_csv(f'stocks/data/{name}.csv',index=False)

    #TODO
    nameDF=pd.read_csv(f'stocks/names.csv')
    nameDF.iat[index,1]=date_to



url='https://www.mse.mk/mk/stats/symbolhistory/ALK'
# driver = webdriver.Chrome()
# driver.get(url)

# filter1(driver)
# filter2()
# filter3(url)
# temp(url)
# driver.quit()
start_date = datetime(2014, 1, 1)
currentday=datetime.today()
name='ALK'
url=f'https://www.mse.mk/mk/stats/symbolhistory/{name}'
update(url, start_date, currentday,name)

