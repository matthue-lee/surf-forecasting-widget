from datetime import date, datetime
from re import M
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import numpy as np

import time

WEIGHTING = {"Surf-Forecast":0.95, "MagicSeaweed":0.8}

driver = webdriver.Chrome(executable_path=r"C:\Windows\chromedriver_win32\chromedriver.exe")

def surf_forecast():
    now = datetime.now()
    today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)

    sf_breaks_dict = {"Bethell's Beach / Te Henga":"https://www.surf-forecast.com/breaks/Bethells-Beach/forecasts/latest/six_day" , "Browns Bay Bar":"https://www.surf-forecast.com/breaks/Browns-Bay-Bar/forecasts/latest/six_day", "Fishermans Reef":"https://www.surf-forecast.com/breaks/Fishermans-Reef/forecasts/latest/six_day", "Karekare":"https://www.surf-forecast.com/breaks/Karekare/forecasts/latest/six_day", "Long Bay Reef":"https://www.surf-forecast.com/breaks/Long-Bay-Reef/forecasts/latest/six_day", "Maori Bay":"https://www.surf-forecast.com/breaks/Maori-Bay/forecasts/latest/six_day", "Matingarahi Point":"https://www.surf-forecast.com/breaks/Matingarahi-Point/forecasts/latest/six_day", "Milford Beach":"https://www.surf-forecast.com/breaks/Milford-Beach/forecasts/latest/six_day", "Muriwai Beach":"https://www.surf-forecast.com/breaks/Muriwai-Beach/forecasts/latest/six_day", "Mussel Rock":"https://www.surf-forecast.com/breaks/Mussel-Rock/forecasts/latest/six_day", "O'Neills Bay":"https://www.surf-forecast.com/breaks/Bethells-Beach-Oneills/forecasts/latest/six_day", "Orere Point":"https://www.surf-forecast.com/breaks/Orere-Point/forecasts/latest/six_day", "Orewa Beach":"https://www.surf-forecast.com/breaks/Orewa-Beach/forecasts/latest/six_day", "Piha North":"https://www.surf-forecast.com/breaks/North-Piha/forecasts/latest/six_day", "Piha-The Bar":"https://www.surf-forecast.com/breaks/Piha-The-Bar/forecasts/latest/six_day", "Piha-The Ditch":"https://www.surf-forecast.com/breaks/Piha-The-Ditch/forecasts/latest/six_day", "Red Beach":"https://www.surf-forecast.com/breaks/Red-Beach/forecasts/latest/six_day", "Rimmers Road":"https://www.surf-forecast.com/breaks/Rimmers-Road/forecasts/latest/six_day", "Shag Rock":"https://www.surf-forecast.com/breaks/Shag-Rock/forecasts/latest/six_day", "Takapuna-North Reef":"https://www.surf-forecast.com/breaks/Takapuna-North-Reef/forecasts/latest/six_day", "Waiheke Island":"https://www.surf-forecast.com/breaks/Waiheke-Island/forecasts/latest/six_day", "Whatipu":"https://www.surf-forecast.com/breaks/Whatipu/forecasts/latest/six_day", "Pakiri": "https://www.surf-forecast.com/breaks/Pakiribeach/forecasts/latest/six_day", "Te Arai Point": "https://www.surf-forecast.com/breaks/Te-Arai-Point/forecasts/latest/six_day","Tawharanui": "https://www.surf-forecast.com/breaks/Tawharanui/forecasts/latest/six_day", "Forestry": "https://www.surf-forecast.com/breaks/Forestry/forecasts/latest/six_day"}
    ratings_dict ={"https://www.surf-forecast.com/staricons/star.0.gif": 0, "https://www.surf-forecast.com/staricons/star.1.gif": 1, "https://www.surf-forecast.com/staricons/star.2.gif": 2, "https://www.surf-forecast.com/staricons/star.3.gif": 3, "https://www.surf-forecast.com/staricons/star.4.gif": 4, "https://www.surf-forecast.com/staricons/star.5.gif": 5}
    sf_breaks_ratings = []#break, rating am, rating pm, size am, size pm
    sf_breaks_np = np.zeros((len(sf_breaks_dict), 5)) # FINISH CONVERTING FROM LIST TO ARRAY 

    driver.get("https://www.surf-forecast.com/breaks/Bethells-Beach/forecasts/latest/six_day")
    for i in range(len(sf_breaks_dict)):
        key = list(sf_breaks_dict)[i]
        sf_breaks_ratings.append(key)
        current_break_url = sf_breaks_dict[key]
        driver.get(current_break_url)
        time.sleep(2)
        #sf_breaks_np[i][0] = key

        if now < today11am:
            rating_element = driver.find_element(By.XPATH, """//*[@id="forecast-table"]/div[2]/table/tbody/tr[3]/td[1]/img""")
        else: 
            rating_element = driver.find_element(By.XPATH, """//*[@id="forecast-table"]/div[2]/table/tbody/tr[3]/td[1]/img""")

        rating_txt = rating_element.get_attribute('src')
        rating_integer = ratings_dict[rating_txt]
        #print(rating_integer)
        sf_breaks_ratings.append(rating_integer)
        #sf_breaks_np[i][1] = rating_integer


        if now < today11am:
            rating_element_pm = driver.find_element(By.XPATH, """//*[@id="forecast-table"]/div[2]/table/tbody/tr[3]/td[2]/img""")
        else:
            rating_element_pm = driver.find_element(By.XPATH, """//*[@id="forecast-table"]/div[2]/table/tbody/tr[3]/td[2]/img""")
        
        rating_txt_pm = rating_element_pm.get_attribute('src')
        rating_integer_pm = ratings_dict[rating_txt_pm]
        sf_breaks_ratings.append(rating_integer_pm)
        #sf_breaks_np[i][2] = rating_integer_pm


        if now < today11am:
            swell_size_am = driver.find_element(By.CSS_SELECTOR, '#forecast-table > div.forecast-table__content > table > tbody > tr:nth-child(5) > td:nth-child(1) > div > svg > text')
        else:
            swell_size_am = driver.find_element(By.CSS_SELECTOR, '#forecast-table > div.forecast-table__content > table > tbody > tr:nth-child(5) > td:nth-child(1) > div > svg > text')
        
        swell_size_txt_am = swell_size_am.text
        sf_breaks_ratings.append(swell_size_txt_am)
        #sf_breaks_np[i][3] = swell_size_txt_am

        if now < today11am:
            swell_size_pm = driver.find_element(By.CSS_SELECTOR, '#forecast-table > div.forecast-table__content > table > tbody > tr:nth-child(5) > td:nth-child(2) > div > svg > text')
        else:
            swell_size_pm = driver.find_element(By.CSS_SELECTOR, '#forecast-table > div.forecast-table__content > table > tbody > tr:nth-child(5) > td:nth-child(2) > div > svg > text')
        
        swell_size_txt_pm = swell_size_pm.text
        sf_breaks_ratings.append(swell_size_txt_pm)
        #sf_breaks_np[i][4] = swell_size_txt_pm

    max_rating_am = 0
    max_rating_pm = 0
    for i in range(0, len(sf_breaks_dict), 5):
        if sf_breaks_ratings[i+1] > max_rating_am:
            max_rating_am = sf_breaks_ratings[i+1]
            max_rated_loc_am = sf_breaks_ratings[i]
            max_am_size = sf_breaks_ratings[i+3]
        if sf_breaks_ratings[i+2] > max_rating_pm:
            max_rating_pm = sf_breaks_ratings[i+2]
            max_rated_loc_pm = sf_breaks_ratings[i]
            max_pm_size = sf_breaks_ratings[i+4] 
    return sf_breaks_ratings

def magic_seaweed():
    ms_breaks_dict = {"Anawhata Beach": "https://magicseaweed.com/Anawhata-Beach-Surf-Report/6933/", "Bethell's Beach / Te Henga": "https://magicseaweed.com/Bethells-Beach-Surf-Report/7145/", "Forestry":"https://magicseaweed.com/Forestry-Surf-Report/122/", "Karekare":"https://magicseaweed.com/Karekare-Beach-Surf-Report/6935/", "Long Bay":"https://magicseaweed.com/Long-Bay-Surf-Report/6931/", "Maori Bay":"https://magicseaweed.com/Maori-Bay-Beach-Surf-Report/6932/", "Milford Beach":"https://magicseaweed.com/Milford-Beach-Surf-Report/6930/", "Orewa Beach":"https://magicseaweed.com/Orewa-Beach-Surf-Report/4079/", "Orewa Rivermouth":"https://magicseaweed.com/Orewa-Rivermouth-Surf-Report/7146/", "Pakiri":"https://magicseaweed.com/Pakiri-Surf-Report/6927/", "Piha":"https://magicseaweed.com/Piha-Surf-Report/90/", "Takapuna": "https://magicseaweed.com/Takapuna-Surf-Report/6774/", "Tawharanui": "https://magicseaweed.com/Tawharanui-Surf-Report/6773/", "Te Arai Point": "https://magicseaweed.com/Te-Arai-Surf-Report/6776/"}
    sf_breaks_dict = {"Bethell's Beach / Te Henga":"https://www.surf-forecast.com/breaks/Bethells-Beach/forecasts/latest/six_day" , "Browns Bay Bar":"https://www.surf-forecast.com/breaks/Browns-Bay-Bar/forecasts/latest/six_day", "Fishermans Reef":"https://www.surf-forecast.com/breaks/Fishermans-Reef/forecasts/latest/six_day", "Karekare":"https://www.surf-forecast.com/breaks/Karekare/forecasts/latest/six_day", "Long Bay Reef":"https://www.surf-forecast.com/breaks/Long-Bay-Reef/forecasts/latest/six_day", "Maori Bay":"https://www.surf-forecast.com/breaks/Maori-Bay/forecasts/latest/six_day", "Matingarahi Point":"https://www.surf-forecast.com/breaks/Matingarahi-Point/forecasts/latest/six_day", "Milford Beach":"https://www.surf-forecast.com/breaks/Milford-Beach/forecasts/latest/six_day", "Muriwai Beach":"https://www.surf-forecast.com/breaks/Muriwai-Beach/forecasts/latest/six_day", "Mussel Rock":"https://www.surf-forecast.com/breaks/Mussel-Rock/forecasts/latest/six_day", "O'Neills Bay":"https://www.surf-forecast.com/breaks/Bethells-Beach-Oneills/forecasts/latest/six_day", "Orere Point":"https://www.surf-forecast.com/breaks/Orere-Point/forecasts/latest/six_day", "Orewa Beach":"https://www.surf-forecast.com/breaks/Orewa-Beach/forecasts/latest/six_day", "Piha":"https://www.surf-forecast.com/breaks/Piha-The-Bar/forecasts/latest/six_day", "Red Beach":"https://www.surf-forecast.com/breaks/Red-Beach/forecasts/latest/six_day", "Rimmers Road":"https://www.surf-forecast.com/breaks/Rimmers-Road/forecasts/latest/six_day", "Shag Rock":"https://www.surf-forecast.com/breaks/Shag-Rock/forecasts/latest/six_day", "Takapuna":"https://www.surf-forecast.com/breaks/Takapuna-North-Reef/forecasts/latest/six_day", "Waiheke Island":"https://www.surf-forecast.com/breaks/Waiheke-Island/forecasts/latest/six_day", "Whatipu":"https://www.surf-forecast.com/breaks/Whatipu/forecasts/latest/six_day", "Pakiri": "https://www.surf-forecast.com/breaks/Pakiribeach/forecasts/latest/six_day", "Te Arai Point": "https://www.surf-forecast.com/breaks/Te-Arai-Point/forecasts/latest/six_day","Tawharanui": "https://www.surf-forecast.com/breaks/Tawharanui/forecasts/latest/six_day", "Forestry": "https://www.surf-forecast.com/breaks/Forestry/forecasts/latest/six_day"}
    ms_breaks_ratings = [[0 for x in range(3)] for y in range(len(ms_breaks_dict))] 
    print(ms_breaks_ratings)

    for i in range(len(ms_breaks_dict)):
        key = list(ms_breaks_dict)[i]
        ms_breaks_ratings[i][0] = key
        current_break_url = ms_breaks_dict[key]
        driver.get(current_break_url)
        time.sleep(2)
        star_vals = []
        s1 = driver.find_element(By.CSS_SELECTOR, "body > div.cover > div.cover-inner > div.pages.clear-left.clear-right > div > div.msw-fc.msw-js-forecast > div:nth-child(2) > div:nth-child(2) > div > div > div.msw-col-fluid > div > div.row.margin-bottom > div.col-lg-7.col-md-7.col-sm-12.col-xs-12.msw-fc-current > div > div.col-lg-7.col-md-7.col-sm-7.col-xs-12 > ul.rating.rating-large.clearfix > li:nth-child(2)")
        star_vals.append(s1.get_attribute('class'))
        s2 = driver.find_element(By.CSS_SELECTOR, "body > div.cover > div.cover-inner > div.pages.clear-left.clear-right > div > div.msw-fc.msw-js-forecast > div:nth-child(2) > div:nth-child(2) > div > div > div.msw-col-fluid > div > div.row.margin-bottom > div.col-lg-7.col-md-7.col-sm-12.col-xs-12.msw-fc-current > div > div.col-lg-7.col-md-7.col-sm-7.col-xs-12 > ul.rating.rating-large.clearfix > li:nth-child(3)")
        star_vals.append(s2.get_attribute('class'))
        s3 = driver.find_element(By.CSS_SELECTOR, "body > div.cover > div.cover-inner > div.pages.clear-left.clear-right > div > div.msw-fc.msw-js-forecast > div:nth-child(2) > div:nth-child(2) > div > div > div.msw-col-fluid > div > div.row.margin-bottom > div.col-lg-7.col-md-7.col-sm-12.col-xs-12.msw-fc-current > div > div.col-lg-7.col-md-7.col-sm-7.col-xs-12 > ul.rating.rating-large.clearfix > li:nth-child(4)")
        star_vals.append(s3.get_attribute('class'))
        s4 = driver.find_element(By.CSS_SELECTOR, "body > div.cover > div.cover-inner > div.pages.clear-left.clear-right > div > div.msw-fc.msw-js-forecast > div:nth-child(2) > div:nth-child(2) > div > div > div.msw-col-fluid > div > div.row.margin-bottom > div.col-lg-7.col-md-7.col-sm-12.col-xs-12.msw-fc-current > div > div.col-lg-7.col-md-7.col-sm-7.col-xs-12 > ul.rating.rating-large.clearfix > li:nth-child(5)")
        star_vals.append(s4.get_attribute('class'))
        s5 = driver.find_element(By.CSS_SELECTOR, "body > div.cover > div.cover-inner > div.pages.clear-left.clear-right > div > div.msw-fc.msw-js-forecast > div:nth-child(2) > div:nth-child(2) > div > div > div.msw-col-fluid > div > div.row.margin-bottom > div.col-lg-7.col-md-7.col-sm-12.col-xs-12.msw-fc-current > div > div.col-lg-7.col-md-7.col-sm-7.col-xs-12 > ul.rating.rating-large.clearfix > li:nth-child(6)")
        star_vals.append(s5.get_attribute('class'))

        rating = 0
        for item in star_vals:
            if item == "active":
                rating += 1
        ms_breaks_ratings[i][1] = rating

        max = 0
        max_loc = ""
    
    for i in range(len(ms_breaks_dict)):
        if ms_breaks_ratings[i][1] > max:
            max = ms_breaks_ratings[i][1]
            max_loc = ms_breaks_ratings[i][0]

    return ms_breaks_ratings

def findTheDifference(s, t):
    diff = []
    for key in s:
        diff.append(key)
    for key in t:
        if (diff.count(key) == 0):
            diff.append(key)
        else:
            diff.remove(key)
    return diff

def findIntersection(s, t):
    intersect = []
    for key in s:
        intersect.append(key)
    for i in intersect:
        if not i in t:
            intersect.remove(i)
    return(intersect)

def findAverageBest():
    ms_ratings = magic_seaweed()
    sf_ratings = surf_forecast()
    
    
    max_rating_am = 0
    max_rating_pm = 0
    for i in range(0, len(sf_breaks_dict), 5):
        if sf_breaks_ratings[i+1] > max_rating_am:
            max_rating_am = sf_breaks_ratings[i+1]
            max_rated_loc_am = sf_breaks_ratings[i]
            max_am_size = sf_breaks_ratings[i+3]
        if sf_breaks_ratings[i+2] > max_rating_pm:
            max_rating_pm = sf_breaks_ratings[i+2]
            max_rated_loc_pm = sf_breaks_ratings[i]
            max_pm_size = sf_breaks_ratings[i+4] 


print ("hellow world")
findAverageBest()