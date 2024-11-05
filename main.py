import time
from threading import Thread
from warnings import catch_warnings

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
from bs4 import BeautifulSoup as bs


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


def filter2():
    df=pd.read_csv('stocks/names.csv')
    n=df.Names[0]
    try:
        temp=pd.read_csv(f'stocks/files/{n}')
        df.iat[0,1]=temp.Date[-1]
    except:
        print(2)
        df.iat[0, 1]=None

    df.to_csv('stocks/names.csv', index=False)

    pass


def filter3(url):
    #scrape the data
    # df=pd.read_csv('stocks/names.csv')
    # for n in df.Names:
    # df = pd.read_csv('stocks/names.csv')
    # n = df.Names[0]
    # Input=driver.find_element(By.ID,'Code')
    # Input.send_keys(n)
    # btn=driver.find_element(By.CLASS_NAME,'btn-primary-sm')
    # btn.click()
    # try:
    #     # Wait until the expected table rows are present
    #     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
    #
    #     # Re-fetch the elements after waiting
    #     elements = driver.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header rows
    #
    #     # Iterate through the rows and extract cell text
    #     for e in elements:
    #         # Re-fetch cells for the current row
    #         cells = e.find_elements(By.TAG_NAME, 'td')
    #         if cells:  # Ensure there are cells to avoid index errors
    #             print(cells[0].text)
    # except Exception as e:
    #     print(f"An error occurred while processing {n}: {e}")
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


    # lastPrice=elements[1].text
    # max=elements[2].text
    # min=elements[3].text
    # volume=elements[6].text
    # tBest=elements[7].text
    # print(date)
    # print(lastPrice)
    # print(max)
    # print(min)
    # print(volume)
    # print(tBest)


    pass


def temp(url):
    df = pd.read_csv('stocks/names.csv')
    name=df.Names[0]
    url = f'https://www.mse.mk/mk/stats/symbolhistory/{name}'
    resp=requests.get(url)
    soup=bs(resp.text, 'html.parser')
    data=[]
    products=soup.find_all('tr',)[2:]
    for p in products:
        print(p.text)

def temp2():
    df = pd.read_csv('stocks/names.csv')
    name = df.Names[0]
    url = f'https://www.mse.mk/mk/stats/symbolhistory/{name}'
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        # Wait until the expected table rows are present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        table = driver.find_element(By.ID, 'results')
        # Re-fetch the elements after waiting
        elements = table.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header rows

        # Iterate through the rows and extract cell text
        for e in elements:
            # Re-fetch cells for the current row
            print(e.text)
            # cells = e.find_elements(By.TAG_NAME, 'td')
            # if cells:  # Ensure there are cells to avoid index errors
            #     print(cells[0].text)
    except Exception as e:
        print(f"An error occurred while processing {name}:")
    # Iterate through each name in the DataFrame
    for n in df.Names:

        Input = driver.find_element(By.ID, 'Code')
        # Input.clear()  # Clear previous input
        Input.send_keys(n)
        btn = driver.find_element(By.CLASS_NAME, 'btn-primary-sm')
        btn.click()

        table = driver.find_element(By.ID, 'results')  # Adjust this locator to match your table
        ActionChains(driver).move_to_element(table).click().perform()

        # time.sleep(200)

        # Wait for the table rows to load after clicking the button
        try:
            # Wait until the expected table rows are present
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

            # Re-fetch the elements after waiting
            elements = table.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header rows

            # Iterate through the rows and extract cell text
            for e in elements:
                # Re-fetch cells for the current row
                print(e.text)
                # cells = e.find_elements(By.TAG_NAME, 'td')
                # if cells:  # Ensure there are cells to avoid index errors
                #     print(cells[0].text)
        except Exception as e:
            print(f"An error occurred while processing {n}: {e}")

url='https://www.mse.mk/mk/stats/symbolhistory/ALK'
# driver = webdriver.Chrome()
# driver.get(url)

# filter1(driver)
# filter2()
filter3(url)
# temp(url)
# driver.quit()

