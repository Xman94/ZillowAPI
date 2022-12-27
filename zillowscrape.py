import re
import pandas as pd #manipulate data
import requests #to get data
import json #for formatting
import time #to control request pace

# show all columns
pd.set_option('display.max_columns', None)

# Prompt the user for an address
address = input("Enter an address copied from google: ")

# Extract the zip code and state from the address
zipcode_state = re.search(r'\d{5}', address)
zipcode = zipcode_state.group()
state = address.split(",")[-1].strip()

# create an empty dataframe to store the results from all iterations
results = pd.DataFrame()

#create a list of home types you want to target
home_types = ["Houses", "Townhomes"]

#create a list of price ranges to extract more data
price_ranges = [[1001, 1250],
                [1251, 1500], [1501, 1750], [1751, 2000], [2001, 2250], [2251,2500],
                [2501, 2750], [2751, 3000], [3001, 3250], [3251, 3500], [3501, 3750],
                [3751, 4000], [4001, 4250], [4251, 4500], [4501, 4750], [4751, 5000]
                ]

#iterate through the home types
for home_type in home_types:
  # Iterate through the price ranges
  for price_range in price_ranges:
    time.sleep(1)
    min_price, max_price = price_range
    key ='46513c8146msh5354f58cab06275p1ac1dcjsnd5b55f931f6f'
    search_str = zipcode + ', ' + state
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    querystring = {"location":search_str,
                "status_type":"ForRent",
                "home_type":home_type,
                "rentMinPrice": min_price,
                "rentMaxPrice": max_price}
    headers = {
        'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
        'x-rapidapi-key': key
        }
    print('query hit')
    z_for_rent_resp = requests.request("GET", url, headers=headers, params=querystring)
    z_for_rent_resp_json = z_for_rent_resp.json()
    # Check for results, if there aren't any, then continue to the next price range.
    if z_for_rent_resp_json['totalResultCount'] == 0:
        continue
    else:
      # This response will retrieve data in a single line. transform to json for readability.
      print('query string successful')
      #z_for_rent_resp_json = z_for_rent_resp.json()
      print('query to data frame')

      # Convert to dataframe using the props key which contains the nested data from the response.
      df_z_for_rent = pd.json_normalize(data=z_for_rent_resp_json['props'])
      print(df_z_for_rent)
    
      print('Number of rows:', len(df_z_for_rent))

      # get zpids to a list
      zpid_list = df_z_for_rent['zpid'].tolist()
      zpid_list

      # create empty list
      prop_detail_list = []
      print('creating list of details')
      # iterate through list of properties
      for zpid in zpid_list:

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
print('Scrape Complete!')
print(results)
