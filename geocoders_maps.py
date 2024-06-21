import re
import time
import folium
import numpy as np
import pandas as pd
from geopy.geocoders import ArcGIS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('Property_Location.csv')

df["Location"] = df["Location"].str.replace(' ','+')
df["Region"] = df["Region"].str.replace(' ','+')

print("Shape of Data :",df.shape)
df.head()

location = []
def Location_Locate():
    for i in range(0,len(df["Location"])):
        try:
            locator = Nominatim(user_agent="streamlitdemo")
            geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
            location.append(geocode(df['Location'][i]))
        except:
            locator = Nominatim(user_agent="streamlitdemo")
            geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
            location.append(geocode(df['Region'][i]))
        else:
            pass
Location_Locate()

Latitude = []
Longitude = []
for i in range(0,len(location)):
    if(location[i]):
        Latitude.append(location[i].latitude)
        Longitude.append(location[i].longitude)
    else:
        Latitude.append(np.nan)
        Longitude.append(np.nan)
print("Total Latitude : ", len(Latitude))

"""#### Adding Latitude and Longitude to the dataframe"""

df['Latitude'] = Latitude
df['Longitude'] = Longitude

df["Location"] = df["Location"].str.replace('+', ' ')
df["Region"] = df["Region"].str.replace('+', ' ')

df.head()

df.isna().sum()

df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df.shape

df.to_csv('Map_Location.csv', index=False)

df2 = pd.read_csv('Map_Location.csv')
df2

lat = list(df2['Latitude'])
lon = list(df2['Longitude'])
name = list(df2['Property_Name'])
add = list(df2['Location'])
price = list(df2['Price'])
age = list(df2['Property_Age'])
avail = list(df2['Availability'])
rate = list(df2['Rate_SqFt'])

gmap = folium.Map(location=[19.25029770723734, 73.13414632644128], zoom_start=10)
fg = folium.FeatureGroup(name="My Map").add_to(gmap)

for lat,lon,name,add,price,age,avail,rate in zip(lat,lon,name,add,price,age,avail,rate):
    html = f"""<p style="color:green" > Property Name : {name}<p/>
               <p style="color:green" > Address : {add}<p/>
               <p style="color:red" > Price : {price}<p/>
               <p style="color:red" > Rate SqFt : {rate}<p/>
               <p style="color:blue" > Property Age : {age}<p/>
               <p style="color:blue" > Availability : {avail}<p/>
            """
    iframe = folium.IFrame(html, width=250, height=270)
    popup = folium.Popup(iframe, max_width=300)
    marker = folium.Marker([lat,lon], popup=(popup)).add_to(gmap)
    gmap.add_child(marker)

gmap.add_child(fg)
gmap.save("mumbai_property.html")

gmap.add_child(fg)
