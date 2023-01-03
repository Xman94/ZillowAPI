# ZillowAPI
This code connects to an api through the RapidAPI marketplace that retrieves data on homes for rent in a specific area. It uses the Zillow API to search for homes based on home type (e.g. houses, townhomes), location, and availability status. The code then iterates through the properties and retrieves detailed information about each one and appends the details to a csv and prepares for download. You can review the endpoints offered on the API homepage to change the code as needed.

## Requirements:
- Python 3
- requests
- pandas
- re
- json
- Google Colab

## How to use:
- Use Git to clone the repo.
- Obtain an API key from https://rapidapi.com/apimaker/api/zillow-com1/ by signing up for a RapidAPI account.
- Replace 'Yourkey' on line 37 with your API key.
- Run the code in a Python environment and enter an address when prompted. The zip code and state of the address will be extracted and used to search for homes in the area.
- The code will retrieve data on homes for rent and store it in a Pandas dataframe. The data includes details such as the property address, number of bedrooms and bathrooms, square footage, and price.
- The data will be saved to a CSV file in the current working directory.
## Notes
- The Zillow API has rate limits, so the code includes a 1 second delay between requests to avoid exceeding the limit.
- The code currently searches for houses and townhomes. To search for other home types, add them to the home_types list on line 13.
- The script will prompt the user for an address, but it is crucial to note the address must be formatted as "address, city, state 5-digit zip" e.g: 500 W 2nd St, Austin, TX 78701
