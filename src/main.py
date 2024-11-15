import requests
import pandas as pd
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

    with open('house_links.csv') as file:
        urls = [(url.strip('\n'), session, headers) for url in file.readlines() if url is not None]
        with Pool() as pool:
            results = [res for res in pool.starmap(get_house_data, urls) if res is not None]
    pd.DataFrame(results, columns=results[0].keys()).to_csv('house_data.csv')
