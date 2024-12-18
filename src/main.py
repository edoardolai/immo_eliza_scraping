import requests
import pandas as pd
from multiprocessing import Pool
from os.path import exists
from utils.get_house_data_scraper import get_house_data
from utils.get_links_data_scraper import get_links_from_page
from utils.clean_data import clean_data_set
from utils.clean_data import clean_data_set
from utils.display_dataframe_info import display_dataframe_info
import json

# Start session
session = requests.Session()
with open('config.json', 'r') as file:
    config = json.load(file)

#Set cookies
cookies = config['cookies']
#Set headers
headers = config['headers']
session.cookies.update(cookies)
session.headers.update(headers)
if __name__ == '__main__':
    if not exists('house_links.csv'):
        base_url_1 = 'https://www.immoweb.be/en/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&minPrice=10000maxPrice=200000&page={}&orderBy=relevance'
        base_url_2 = 'https://www.immoweb.be/fr/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&maxPrice=20000000&minPrice=200000&page={}&orderBy=relevance'
        pages_1 = [(base_url_1.format(page),session) for page in range(334)]
        pages_2 = [(base_url_2.format(page),session) for page in range(334)]

        all_pages = pages_1 + pages_2

        with Pool() as pool: 
            all_links = pool.starmap(get_links_from_page, all_pages)
            flat_links = [link for sub_list in all_links for link in sub_list]
        with open('house_links.csv', mode='w') as file:
            file.writelines(flat_links)
    if not exists('house_data.csv'):
        with open('house_links.csv') as file:
            urls = [(url.strip('\n'), session) for url in file.readlines() if url is not None]
            with Pool() as pool:
                results = [res for res in pool.starmap(get_house_data, urls) if res is not None]
        pd.DataFrame(results, columns=results[0].keys()).to_csv('house_data.csv')

    if exists('house_data.csv'):
        df = pd.read_csv('house_data.csv')
        clean_data_set(df)
        cleaned_df = pd.read_csv('house_data_clean.csv',dtype={
        'locality': str,
        'id': str,
        'zip_code': str,
        'property_type': str,
        'state_of_building': str,
        'price': float,
        'nb_bedrooms': 'Int64',
        'living_area': 'Int64',
        'surface_of_the_plot': 'Int64',
        'nb_facades': 'Int64',
        'garden_surface': 'Int64',
        'terrace_surface': 'Int64',
        'fireplace': int,
        'Equipped kitchen': int,
        'garden': int,
        'terrace': int,
        'furnished': int,
        'swimming_pool': int})
        display_dataframe_info(df)