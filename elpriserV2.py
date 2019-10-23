from matplotlib import pyplot as plt
import time
from selenium import webdriver
import pandas as pd
import numpy as np

browser = webdriver.Firefox()

browser.get("https://www.nordpoolgroup.com/Market-data1/Dayahead/Area-Prices/ALL1/Hourly/")

time.sleep(3)

todays_file_name = browser.find_element_by_css_selector("#datatable > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1)").text


with open(str(todays_file_name) + ".csv", "w") as f:
    f.write("hours,price\n")
    
    i = 1
    while i <= 24:
        price = browser.find_element_by_css_selector("tr.data-row:nth-child(" + str(i) + ") > td:nth-child(9)").text.replace(",", ".")
        
        if i == 23:
            f.write(str(i-1))
            f.write(",")
            price = float(price)*7.5
            price = float(price)/10
            f.write(str(price))
            break

        price = float(price)*7.5
        price = float(price)/10
        print(price)
        f.write(str(i-1))
        f.write(",")
        f.write(str(price))
        f.write("\n")
        i += 1

             
browser.close()
print("Data gathered, closing browser...")



data = pd.read_csv(todays_file_name + ".csv")

plt.figure(figsize=(10, 5))

plt.plot(data.hours, data.price)

plt.xticks(np.arange(min(data.hours), max(data.hours)+2, 1.0))
plt.yticks(np.arange(min(data.price), max(data.price)+1, 2.0))

plt.title("Electricity price per hour")
plt.xlabel("Time (in hours)")
plt.ylabel("Price (in danish oere per kWh)")

print("Program done!")
plt.show()
print("Exiting!")