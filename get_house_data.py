import requests
from bs4 import BeautifulSoup as bs
import re
import urllib.parse
import pandas as pd
urls =["https://www.immoweb.be/en/classified/villa/for-sale/zulte-machelen/9870/20311323", "https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311343","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311345","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311337","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311338","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311336","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311340","https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20311344"]

# Locality //regex for Neighborhood\sor\slocality and select next sybling
# Type of property (House/apartment) .classified__title
# Subtype of property (Bungalow, Chalet, Mansion, ...) //optional
# Price .classified_price sr-only
# Type of sale (Exclusion of life sales)
# Number of rooms //regex for (\d)\s(bedrooms)
# Living Area //regex for (\d{2,3})\s(.{2})\s(livable\sspace)
# Surface of the land (\d{2,3})\s(.{2})\s(livable\sspace)
# Surface area of the plot of land
# Number of facades
# State of the building (New, to be renovated, ...) to be done

# Start session and set headers
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', #mimics browser
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', #format of content
    'Accept-Language': 'en-US,en;q=0.5', #preferred language in response 
    'Referer': 'https://www.immoweb.be/en', #previous page that originated the request
}

# Update cookies (these values need to be valid from your browser session)
cookies = {'immoweb_session' : 'eyJpdiI6IjVubHc4Q1R3RlpvRXkwaVVWQkdNZ3c9PSIsInZhbHVlIjoiakZGMjViTnVxTmROYm1GU2ZYUU9XR3NLMjJrTG84cmVkYm1NN2tqSWhCWjFHQjJQNmxHdDBZbnhPS1JsdzBzSmtUdmpWOXhOdllaeTdqRWZhZ0k4cWhwQWw5MGVwZVlZVTlDQ0ZWcHNJR3h6aXZEdFNMZVg3UTVnR0tGWHcyK1UiLCJtYWMiOiIxZDg1ZjRhNTkxODlkM2VhN2Y3MzY2NTdmMDRkYTc5NjAzYzY5YWVkNDAyYTFjMDEzMmQ3ZmI1MGYyYWY4MjBlIn0%3D',
                       'XSRF-TOKEN': 'eyJpdiI6IkxwRzIwZFEzMTg5VzJDYWtvWi8zM3c9PSIsInZhbHVlIjoiNERVU1NhdlEzVzBIbkZ4cmV4Z2JMbHN3NjVrRWZUMzg0OWd1MVd3N1E3ckI5aGhIRVlaa2czWnl4QVdvbjJUSTZxMkhGdlA1ZzA1c0xxU1A0N0hlaS8rZnV4TmxldDVIbHNUZDVNNCtpSS9qb2x3enNodFFITFJGTlZEZVVrN2siLCJtYWMiOiI2MTJmZDcxNzkyM2YwMTM1ZjZkZGRjZTM5YjIzMGFmNTNiNDA1NTAyMmE0OWRhMTBlMzQwMDVjZjY3YmMzNmE3In0%3D',
                       '__cf_bm' : 'MoKFFUtnsCnBMVsc_XiGba.KtzFY_Ta1f6UtGsI_7j4-1731414232-1.0.1.1-0sQuyt.MEHq3govqH2hn5G0QTGypm5VhAs_Bbhx8a1jvPdIz6yUY5HZKXWDlbV8WF2w.FVvnEgBOUdzQ46C3Rw'}

session.cookies.update(cookies)

def extract_table_data(page, regex):
    searched_tag = page.find('th',string = re.compile(regex))
    if searched_tag is not None:
        return page.find('th',string = re.compile(regex)).next_sibling.next_element.next_element.strip()
    else:
        return None

def get_house_data(url: str, session):
    response = session.get(url, headers=headers)
    house_dict= dict()
    if response.status_code == 200:
        house_page = bs(response.content, 'html.parser')
        cleaned_url = re.sub(r"[^\w\s()\u00C0-\u017F-]/+|[\s']*",'',urllib.parse.unquote(url))
        house_dict['locality'] = re.findall(r'for-sale/(\w+([-\w*])*)', urllib.parse.unquote(cleaned_url))[0][0].title() #usually next sybling is \n
        house_dict['property_type'] = re.findall(r'(classified)/(\w+)',cleaned_url)[0][1].title()
        house_dict['price'] = house_page.select_one('.classified__price .sr-only').get_text().strip('€')
        house_dict['nb_bedrooms'] = extract_table_data(house_page, r'Bedrooms')
        house_dict['living_area'] = extract_table_data(house_page, r'Living\sarea')
        house_dict['surface_of_land'] = extract_table_data(house_page, r'Surface\sof\sthe\splot')
        house_dict['nb_facades'] = extract_table_data(house_page, r'Number\sof\sfrontages')
        house_dict['state_of_building'] = extract_table_data(house_page, r'Building\scondition')
        print(house_dict)
        return house_dict
    else:
        print(f"Failed to fetch {url}: {response.status_code}")

# file = pd.read_csv('test.csv')
dictionaries = list()

with open('test.csv') as file:
    for url in file.readlines():
        dictionaries.append(get_house_data(url, session))

print(dictionaries)