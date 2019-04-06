#!/usr/bin/env python
# coding: utf-8

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import os

import sys
sys.path.append('/Users/flowe/Desktop/Northwestern/NUCHI201902DATA3/NW-Bootcamp-Projects')

import csv

# for progress bars
from tqdm import tqdm, tqdm_pandas
tqdm_pandas(tqdm())

# API Key
from config import api_key

#ZillowWrapper
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults


#Read csv
address_zip_df = pd.read_csv('ChicagoAddress.csv').dropna()
address_zip_df.head()

test_data = address_zip_df

test_data.shape

address_zip_df.shape



address = '233 E 13th St 2207'
zipcode = '60605'

zillow_data = ZillowWrapper(api_key)
response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(response)
print(result.zestimate_valuation_range_high) #no
print(result.zestimate_valuationRange_low)#no
print(result.zestimate_value_change) #yes last 30 days
print(result.home_detail_link)#no
print(result.property_size) #yes
print(result.home_size) #no

bad_address = "234 Ashland"
bad_zip = "60605"


good_address = "125 E 13th St 1001"
good_zip = "60605"


zillow_data = ZillowWrapper(api_key)

def get_zillow_info(address,zipcode):
    try:
        response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(response)
        
        # get zillow_id value
        try:
            zillow_id = result.zillow_id
        except AttributeError: 
            zillow_id = None
        
        # get tax value
        try:
            tax = result.tax_value
        except AttributeError: 
            tax = None
            
        # get latitude
        try:
            tax_year = result.tax_year
        except AttributeError:
            tax_year = None
            
        # 4home type 
        try:    
            home_type = result.home_type
        except AttributeError:
            home_type = None
            
        # 5 property size
        try:    
            property_size = result.property_size
        except AttributeError:
            property_size = None
        
        # 6 bathrooms
        try:    
            bathrooms = result.bathrooms
        except AttributeError:
            bathrooms = None
        
        # 7 bedrooms
        try:    
            bedrooms = result.bedrooms
        except AttributeError:
            bedrooms = None
            
        # 8last sold date
        try:    
            last_sold_date = result.last_sold_date
        except AttributeError:
            last_sold_date = None
        
        # 9last sold price
        try:    
            last_sold_price = result.last_sold_price
        except AttributeError:
            last_sold_price = None
            
       # 10zestimate amount
        try:    
            zestimate_amount = result.zestimate_amount
        except AttributeError:
            zestimate_amount = None
        # 11zestimate last updated
        try:    
            zestimate_last_updated = result.zestimate_last_updated
        except AttributeError:
            home_type = None
        # 12zestimate value change
        try:    
            zestimate_value_change = result.zestimate_value_change
        except AttributeError:
            zestimate_value_change = None
        
        final = [zillow_id,tax,tax_year,home_type,
                 property_size,bathrooms,bedrooms,
                 last_sold_date,last_sold_price,zestimate_amount,
                 zestimate_last_updated,zestimate_value_change]
        
    except:
        final = []
    return final


get_zillow_info(bad_address,bad_zip)



address_zip_df["zillow_info"] = address_zip_df.progress_apply(lambda row: get_zillow_info(row["Address"],row["Zip"]),axis=1)


address_zip_df.head()#["zillow_info"][10][10]


# turn the zillow_info column which is a list into dataframe
zillow_info_df = pd.DataFrame(address_zip_df.zillow_info.values.tolist())


zillow_info_df.head()



# CHANGE COLUMN NAME
# zillow_info_df = zillow_info_df.rename(columns={0:"Zillow ID", 1:"Tax"})
zillow_info_df = zillow_info_df.rename(columns={0:"Zillow ID",1:"Tax",2:"Tax_Year",3:"Home Type",4:"Home Size",5:"Bathrooms",6:"Bedrooms",7:"Last Sold Date",8:"Last Sold Price",9: "Zestimate Amount",10:"Zestimate Date",11:"Zestimate Value Change"})
#df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
zillow_info_df



# combine zillow info dataframe with address info, to make sure they line up
final_zillow = pd.concat([address_zip_df,
                          zillow_info_df],axis=1)


# check results
final_zillow.head()


# check file path, just like `pwd` in terminal 
import os
os.getcwd()


# drop zillow_info column AND save file
final_zillow.drop(columns=["zillow_info"]).to_csv("final_zillow_info.csv",index=None)

