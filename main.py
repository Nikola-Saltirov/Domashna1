from threading import Thread
from warnings import catch_warnings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import threading
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
from winerror import NOERROR


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


def filter3(driver):
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

    # Iterate through each name in the DataFrame
    for n in df.Names:
        # Input the name in the search box
        Input = driver.find_element(By.ID, 'Code')
        # Input.clear()  # Clear previous input
        Input.send_keys(n)

        # Click the search button
        btn = driver.find_element(By.CLASS_NAME, 'btn-primary-sm')
        btn.click()

        # Wait for the table rows to load after clicking the button
        try:
            # Wait until the expected table rows are present
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

            # Re-fetch the elements after waiting
            elements = driver.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header rows

            # Iterate through the rows and extract cell text
            for e in elements:
                # Re-fetch cells for the current row
                cells = e.find_elements(By.TAG_NAME, 'td')
                if cells:  # Ensure there are cells to avoid index errors
                    print(cells[0].text)
        except Exception as e:
            print(f"An error occurred while processing {n}: {e}")


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



url='https://www.mse.mk/mk/stats/symbolhistory/KMB'
driver = webdriver.Chrome()
driver.get(url)

# filter1(driver)
# filter2()
filter3(driver)

driver.quit()

