from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import re
import pandas as pd #manipulate data
import requests #to get data
import json #for formatting
import time #to control request pace
      
class ZillowAPI:
    def __init__(self):
        results = pd.DataFrame()
        key = "46513c8146msh5354f58cab06275p1ac1dcjsnd5b55f931f6f"
        # show all columns
        pd.set_option('display.max_columns', None)
        # self.coordinates = ""
        # while self.coordinates == "":
        #     self.coordinates = input('Please Enter lat/lon coordinates: ')
        self.coordinates = '30.276915386675846, -97.70314872418832'
            
        # Split the input into separate variables for latitude and longitude
        lat, lon = self.coordinates.split(", ")
        
        # Set up the API request
        url = "https://zillow-com1.p.rapidapi.com/propertyByCoordinates"
        querystring = {"lat": lat, 
                       "long": lon, 
                       "d": "0.1", 
                       "includeSold": "0"}
        headers = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        # Make the API request
        z_for_rent_resp = requests.request("GET", url, headers=headers, params=querystring)
        
        # Check if the response is empty
        if not z_for_rent_resp:
            print("Error: API request returned no response")
        else:
            print('query string successful')
            
        #convert the single line response to json
        z_for_rent_resp_json = z_for_rent_resp.json()
        print('query to data frame')
        # print(z_for_rent_resp_json)
        response_dict = z_for_rent_resp_json
        df_z_for_rent = pd.DataFrame.from_dict(response_dict)
        print(df_z_for_rent)

        # get zpids to a list
        zpids = []
        
        for item in z_for_rent_resp_json:
            zpids.append(item['property']['zpid'])
        
        print(zpids)
        # create empty list
        prop_detail_list = []
        print('creating list of details')
        # iterate through list of properties
        for zpid in zpids:
    
            # end point
            url = "https://zillow-com1.p.rapidapi.com/property"
    
            querystring = {"zpid":zpid}
    
            # header
            headers = {
                'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
                'x-rapidapi-key': key
                }
    
            # get property detail. For each Zpid, get the data from the endpoint and transform to json.
            z_prop_detail_resp = requests.request("GET", url, headers=headers, params=querystring)
            z_prop_detail_resp_json = z_prop_detail_resp.json()
    
            # wait 1 sec based on limit
            time.sleep(0.75)
            #append the json response to the list.
            prop_detail_list.append(z_prop_detail_resp_json)
    
        # convert to dataframe
        print('converting details to dataframe')
        df_z_prop_detail = pd.json_normalize(prop_detail_list)
    
        # columns of interest
        detail_cols = ['brokerageName', 
        'streetAddress',
        'livingArea',
        'bedrooms',
        'bathrooms',
        'resoFacts.parkingFeatures',
        'price',
        'yearBuilt',
        'homeType',
        'resoFacts.highSchoolDistrict',
        'url',
        'longitude',
        'latitude',
        'zipcode']
    
        # retain limited columns for output
        df_z_prop_detail_output = df_z_prop_detail[detail_cols]
          
        # append data to results dataframe
        results = results.append(df_z_prop_detail_output)
        print('appending')
        # download file
        print(results)

        
    

if __name__ == "__main__":
    ZillowAPI()
    