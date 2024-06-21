## 1. Import Necessary Libraries
import re
import string
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

"""### 2. Import the Dataset"""

raw_data = pd.read_csv("Raw_Property.csv")
raw_data

"""### 3. Data Preprocessing
#### 3.1 Remove the Unwantend Symbols and Text
"""

raw_data["Property_Age"] = raw_data["Property_Age"].str.replace(' Old','')

raw_data["Rate_SqFt"] = raw_data["Rate_SqFt"].str.replace(',','')

raw_data["Availability"] = raw_data["Availability"].str.title()
raw_data["Availability"] = raw_data["Availability"].str.replace(' Property','')
raw_data["Availability"] = [i.lstrip() for i in raw_data["Availability"]]

raw_data.Availability.unique()

"""#### 3.2 Set Colum Area in SqFt"""

area=[]
for i in range(2581):
    clean_sqft = re.sub('[^0-9.]', " ", raw_data["Area_Tpye"][i])
    area.append(clean_sqft.split()[0])
raw_data['Area_SqFt']=area

"""#### 3.3 Set Colum Type of Carpet Area"""

carpet=[]
for i in range(2581):
    clean_carpet = re.sub('[^a-zA-Z]', " ", raw_data['Area_Tpye'][i])
    carpet.append(clean_carpet.split()[0]+' '+clean_carpet.split()[1])
raw_data['Area_Tpye']=carpet

raw_data['Area_Tpye'] = raw_data.Area_Tpye.str.title()

raw_data['Area_Tpye'] = raw_data.Area_Tpye.str.replace('Super Built','Super Built Up')
raw_data['Area_Tpye'] = raw_data.Area_Tpye.str.replace('Built Up','Built Up Area')
raw_data['Area_Tpye'] = raw_data.Area_Tpye.str.replace('Carpet Area ','Carpet Area')

raw_data.Area_Tpye.unique()

"""#### 3.4 Remove Unwanted Text from Floor No"""

raw_data['Floor_No'] = raw_data.Floor_No.str.replace('Ground','0')
raw_data['Floor_No'] = raw_data.Floor_No.str.replace('Basement','-1')

floor=[]
for i in range(2581):
    clean_sqft = re.sub('[^0-9-]', "", raw_data["Floor_No"][i])
    floor.append(clean_sqft)
raw_data['Floor_No']=floor

"""#### 3.5 Set Colum Region"""

raw_data["Location"] = [i.lstrip() for i in raw_data["Location"]]

location=[]
for i in range(2581):
    clean_location = re.sub('[^a-zA-Z-]', " ", raw_data["Location"][i])
    location.append(clean_location)
raw_data['Region']=location

raw_data['Region'] = raw_data.Region.str.title()
words = ['[0-9]','East','West','South','Suburbs','Sector','Beyond','And Beyond', 'Scheme']
raw_data["Region"] = raw_data["Region"].str.replace('|'.join(words), '', regex=True).str.strip()

raw_data

location=[]
for i in range(2581):
    try:
        location.append(raw_data['Region'][i].split()[-3]+' '+raw_data['Region'][i].split()[-2])
    except:
        location.append(raw_data['Region'][i].split()[-2]+' '+raw_data['Region'][i].split()[-1])
raw_data['Region']=location

raw_data.Region.value_counts().head(30)

add=[]
for i in range(2581):
    clean_add = re.sub('[^a-zA-Z0-9]', " ", raw_data["Location"][i])
    add.append(clean_add)
raw_data['Location']=add

raw_data["Location"] = raw_data["Location"].str.replace('   ',' ')
raw_data["Location"] = raw_data["Location"].str.replace('  ',' ')

raw_data

"""#### 3.6 Replace the all Values in Lac's from Price Column"""

def converter(x):
    if 'Lac' in x:
        return f"{(float(x.strip('Lac'))*1):,.1f}"
    elif 'Crore' in x:
        return f"{(float(x.strip('Crore'))*100):,.1f}"

raw_data['Price_Lakh'] = raw_data['Price'].apply(converter)
raw_data["Price_Lakh"] = raw_data["Price_Lakh"].str.replace(',','')

raw_data.head()

"""#### 3.7 Check The Null Values and Remove"""

raw_data.isna().sum()

raw_data.dropna(inplace=True)
raw_data.reset_index(drop=True, inplace=True)

raw_data = raw_data.to_csv('Property_Location.csv', index=False)

"""#### 3.8 Sort the all Columns"""

raw_data = pd.read_csv('Property_Location.csv')

raw_data = raw_data[['Property_Name','Location','Region','Property_Age','Availability','Area_Tpye','Area_SqFt','Rate_SqFt','Floor_No','Bedroom','Bathroom','Price_Lakh']]
raw_data

"""#### 3.9 Create a Final Clean CSV File"""

property_mumbai = raw_data.to_csv('Mumbai_Property.csv', index=False)

property_mumbai = pd.read_csv('Mumbai_Property.csv')
property_mumbai

"""# The End !!"""