import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from sneakairs.nodes.kof_functions import p_get_data, meta_get_data

def scrape_kof(*args):

    db = []
    linkn = 45
    end = False
    urln = 1

    while end == False:
        #iterate through release date calendars
        try:
            #kof past release date calendar
            url = 'https://www.kicksonfire.com/app/past?page=' + str(urln)
            responseMain = requests.get(url)
            soupMain = BeautifulSoup(responseMain.text, 'html.parser')
        except IndexError:
            end = True
            break
        #iterate through individual shoe websites
        for i in range(0,12):
            try:
                #individual shoe website
                one_a_tag = soupMain.findAll('a')[linkn]
                link = one_a_tag['href']
                response = requests.get(link)
                time.sleep(1)
                soup = BeautifulSoup(response.text, 'html.parser')

                #retrieve number of wants on kicks on fire
                kofWantsn = 2
                kofWants = p_get_data(kofWantsn)

                #retrieve colorway of shoe
                colorn = 4
                color = p_get_data(colorn)

                #retrieve release date of shoe
                daten = 6
                date = p_get_data(daten)
                date = pd.to_datetime(date)

                #retrieve style code of shoe
                styleCoden = 8
                styleCode = p_get_data(styleCoden)

                #retrieve shoe name
                shoen = 5
                shoe = meta_get_data(shoen)

                #retrieve shoe story
                storyn = 6
                story = meta_get_data(storyn)

                #retrieve brand of shoe
                brandn = 15
                brand = meta_get_data(brandn)

                #retrieve retail price of shoe
                pricen = 19
                price = meta_get_data(pricen)

                #create list of complete shoe profile
                profile = [styleCode,shoe,brand,date,price,color,story,kofWants]

                #create list of complete shoe profile with story of shoe
                #profile = [styleCode,shoe,brand,date,price,color,story,kofWants]

                #append profile of shoe to database
                db.append(profile)

                #go to next shoe
                linkn += 1
            except IndexError:
                break
        urln += 1
        linkn = 45

    df = pd.DataFrame(data = db, columns=['code_style','name','brand','date','retail_price','colorway','story','kof_wants'])

    return df

# def p_get_data(number):
#     data = soup.findAll('p')[number].contents[0]
#     return data

# def meta_get_data(number):
#     data = soup.findAll('meta')[number]['content']
#     return data