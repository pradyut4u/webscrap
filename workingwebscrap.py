from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/" 
browser = webdriver.Chrome("chromedriver.exe")
browser.get(url)
time.sleep(10)

headers = ["NAME","LIGHT-YEARS FROM EARTH","PLANET MASS","STELLAR MAGNITUDE","DISCOVERY DATE","Hyperlink","PLANET TYPE","ORBITAL RADIUS","PLANET RADIUS","ORBITAL PERIOD","ECCENTRICITY"]
planetdata = []
newplanetdata = []

def scrap():

    for i in range(1,439):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        currentpagenum = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
        if(currentpagenum < i):
            print("pagenum is less")
            browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a')
            r = scraper(i,soup)
        elif(currentpagenum>i):
            print("pagenum is more")
            browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a')
            t = scraper(i,soup)
        elif(i == currentpagenum):
            y = scraper(i,soup)
        else:
            break

def scraper(i,soup):
    for ul_tag in soup.find_all("ul",attrs = {"class","exoplanet"}):
        li_tags = ul_tag.find_all("li")
        temp = []
        for index,li_tag in enumerate(li_tags):
            if(index == 0):
                temp.append(li_tag.find_all("a")[0].contents[0])      
            else:
                try:
                    temp.append(li_tag.contents[0])
                except:
                    temp.append("")
                
        planetdata.append(temp)
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
    print(f"{i} pageover")
           
    
    with open("planets.csv","w")as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planetdata)
        print("completed")

a = scrap()