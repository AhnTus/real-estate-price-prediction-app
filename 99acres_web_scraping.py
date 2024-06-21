## 1. Import Necessary Libraries
import timeit
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')

"""### 2. Scraping the Properties"""

start = 101
stop  = 111

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

"""#### 2.1 Define a function for each Colums"""

def property_nane(soupy_object):   # return house or property name
    try:
        name = soupy_object.find('span', attrs = {'class':'undefined'}).text
    except:
        name = None
    return name

def address_details(soupy_object):   # return address of property
    try:
        address = soupy_object.find('i', attrs = {'id':'address'}).text
    except:
        address = None
    return address

def total_price(soupy_object):   # return total price of property
    try:
        price = soupy_object.find('span', attrs = {'id':"pdPrice2"}).text
    except:
        price = None
    return price

def rate_sqft(soupy_object):   # return total price of property
    try:
        rate = soupy_object.find('div', attrs = {'id':"pricePerUnitArea"}).text.split(' ')[1]
    except:
        rate = None
    return rate

def area_type(soupy_object):   # return area parameters
    try:
        areatyp = soupy_object.find('div', attrs = {'id':'factArea'}).text
    except:
        areatyp = None
    return areatyp

def bedroom_count(soupy_object):   # return number of bedrooms
    try:
        bedroom = soupy_object.find('span', attrs={"id":"bedRoomNum"}).text.split(' ')[0]
    except:
        bedroom = None
    return bedroom

def bathroom_count(soupy_object):   # return number of bathrooms
    try:
        bathroom =  soupy_object.find('span', attrs= {'id':'bathroomNum'}).text.split(' ')[0]
    except:
        bathroom = None
    return bathroom

def floor_num(soupy_object):   # return number of floor
    try:
        floornum = soupy_object.find('span', attrs = {'id':'floorNumLabel'}).text.split(' ')[0]
    except:
        floornum = None
    return floornum

def property_age(soupy_object):   # return age of property
    try:
        age = soupy_object.find('span', attrs ={'id':'agePossessionLbl'}).text
    except:
        age = None
    return age

def availability(soupy_object):   # return area parameters
    try:
        avail = soupy_object.find('span', attrs = {'id':'Availability_Lbl'}).text
    except:
        avail = None
    return avail

"""#### 2.2 Return a Complete DataFrame into CSV File"""

data_list = []
def get_all(start, stop):
    for pagenubmer in range(start, stop):
        url = f'https://www.99acres.com/property-in-mumbai-ffid-page-{pagenubmer}'
        req = get(url, headers = headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links = soup.find_all('a', attrs= {"class":"body_med srpTuple__propertyName"})

        for k, item in enumerate(links):
            main_url = 'https://www.99acres.com'
            sub_url = item.get('href')
            data_url = main_url + sub_url
            request = get(data_url, headers=headers)
            soup_get = BeautifulSoup(request.content, 'html.parser')

            name = property_nane(soup_get)
            address = address_details(soup_get)
            price = total_price(soup_get)
            rate = rate_sqft(soup_get)
            areatyp = area_type(soup_get)
            bedroom = bedroom_count(soup_get)
            bathroom = bathroom_count(soup_get)
            floornum = floor_num(soup_get)
            age = property_age(soup_get)
            avail = availability(soup_get)

            data = {'Property_Name': name, 'Location': address, 'Price':price, 'Rate_SqFt':rate, 'Area_Tpye':areatyp,
                    'Bedroom': bedroom, 'Bathroom':bathroom, 'Floor_No':floornum, 'Property_Age':age, 'Availability':avail}
            data_list.append(data)

        timestart = timeit.default_timer()
        timestop = timeit.default_timer()
        print(f'You scraped page no : {pagenubmer}')
        print('Time :', timestop - timestart)

    return data_list

"""#### 2.3 Define a DataFrame"""

df1 = pd.DataFrame(get_all(start, stop))

"""#### 2.4 Data Understanding"""

df1.head()

df1.info()

df1.duplicated().sum()

df1.nunique()

"""#### 2.5 Create a CSV File"""

df1.to_csv('Prop_101to110.csv', index_label = False)

projectlist = pd.read_csv("Prop_101to110.csv")
projectlist.head(16)

"""### 3. Import the all Datasets and Concating"""

df1 = pd.read_csv("Prop_001to050.csv")
df2 = pd.read_csv("Prop_051to100.csv")
df3 = pd.read_csv("Prop_101to150.csv")

df = pd.concat([df1, df2, df3], ignore_index=False)

df

df["Property_Name"] = df["Property_Name"].str.replace('Toll Free 1800 41 99099','Unnamed Property')

df.isna().sum()

df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df.isna().sum()

df.duplicated().sum()

df = df.drop_duplicates(ignore_index=True)

df.to_csv('Raw_Property.csv', index=False)

df = pd.read_csv('Raw_Property.csv')

print('Shape of Data :', df.shape)
df

"""# The End !!!"""