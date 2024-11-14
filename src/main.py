import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from multiprocessing import Pool
from os.path import exists
from utils.get_house_data_scraper import get_house_data
from utils.get_links_data_scraper import get_links_from_page


# Start session and set headers
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', #mimics browser
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', #format of content
    'Accept-Language': 'en-US,en;q=0.5', #preferred language in response 
    'Referer': 'https://www.immoweb.be/en', #previous page that originated the request
}

# Set cookies for request
cookies = {'immoweb_session' : 'eyJpdiI6IjVubHc4Q1R3RlpvRXkwaVVWQkdNZ3c9PSIsInZhbHVlIjoiakZGMjViTnVxTmROYm1GU2ZYUU9XR3NLMjJrTG84cmVkYm1NN2tqSWhCWjFHQjJQNmxHdDBZbnhPS1JsdzBzSmtUdmpWOXhOdllaeTdqRWZhZ0k4cWhwQWw5MGVwZVlZVTlDQ0ZWcHNJR3h6aXZEdFNMZVg3UTVnR0tGWHcyK1UiLCJtYWMiOiIxZDg1ZjRhNTkxODlkM2VhN2Y3MzY2NTdmMDRkYTc5NjAzYzY5YWVkNDAyYTFjMDEzMmQ3ZmI1MGYyYWY4MjBlIn0%3D',
                       'XSRF-TOKEN': 'eyJpdiI6IkxwRzIwZFEzMTg5VzJDYWtvWi8zM3c9PSIsInZhbHVlIjoiNERVU1NhdlEzVzBIbkZ4cmV4Z2JMbHN3NjVrRWZUMzg0OWd1MVd3N1E3ckI5aGhIRVlaa2czWnl4QVdvbjJUSTZxMkhGdlA1ZzA1c0xxU1A0N0hlaS8rZnV4TmxldDVIbHNUZDVNNCtpSS9qb2x3enNodFFITFJGTlZEZVVrN2siLCJtYWMiOiI2MTJmZDcxNzkyM2YwMTM1ZjZkZGRjZTM5YjIzMGFmNTNiNDA1NTAyMmE0OWRhMTBlMzQwMDVjZjY3YmMzNmE3In0%3D',
                       '__cf_bm' : 'MoKFFUtnsCnBMVsc_XiGba.KtzFY_Ta1f6UtGsI_7j4-1731414232-1.0.1.1-0sQuyt.MEHq3govqH2hn5G0QTGypm5VhAs_Bbhx8a1jvPdIz6yUY5HZKXWDlbV8WF2w.FVvnEgBOUdzQ46C3Rw'}

session.cookies.update(cookies)
session.headers = headers
if __name__ == '__main__':
    if(not exists('house_links.csv')):
        base_url = 'https://www.immoweb.be/en/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&minPrice=10000&page={}&orderBy=relevance'
        pages = [(base_url.format(page),session) for page in range(192)]

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
