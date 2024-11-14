import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pathlib import Path
from multiprocessing import Pool
from os.path import exists
from utils.get_house_data_scraper import get_house_data
from utils.get_links_data_scraper import get_links_from_page
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
    if(not exists('house_links.csv')):
        base_url = 'https://www.immoweb.be/en/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&minPrice=10000&page={}&orderBy=relevance'
        pages = [(base_url.format(page),session) for page in range(300)]

        with Pool() as pool: 
            all_links = pool.starmap(get_links_from_page, pages)
        flat_links = [link for sub_list in all_links for link in sub_list] #todo fix this not flattening...
        with open('house_links.csv', mode='w') as file:
            file.writelines(flat_links)

    with open('house_links.csv') as file:
        urls = [(url.strip('\n'), session, headers) for url in file.readlines()]
        with Pool() as pool:
            results = [res for res in pool.starmap(get_house_data, urls) if res is not None]
    pd.DataFrame(results, columns=results[0].keys()).to_csv('house_data.csv')
