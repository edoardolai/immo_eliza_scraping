import requests
import csv
import time
from multiprocessing import Pool

id_numbers = []
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', #mimics browser
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', #format of content
    'Accept-Language': 'en-US,en;q=0.5', #preferred language in response 
    'Referer': 'https://www.immoweb.be/en', #previous page that originated the request
}

cookies = {'immoweb_session' : 'eyJpdiI6IjVubHc4Q1R3RlpvRXkwaVVWQkdNZ3c9PSIsInZhbHVlIjoiakZGMjViTnVxTmROYm1GU2ZYUU9XR3NLMjJrTG84cmVkYm1NN2tqSWhCWjFHQjJQNmxHdDBZbnhPS1JsdzBzSmtUdmpWOXhOdllaeTdqRWZhZ0k4cWhwQWw5MGVwZVlZVTlDQ0ZWcHNJR3h6aXZEdFNMZVg3UTVnR0tGWHcyK1UiLCJtYWMiOiIxZDg1ZjRhNTkxODlkM2VhN2Y3MzY2NTdmMDRkYTc5NjAzYzY5YWVkNDAyYTFjMDEzMmQ3ZmI1MGYyYWY4MjBlIn0%3D',
                    'XSRF-TOKEN': 'eyJpdiI6IkxwRzIwZFEzMTg5VzJDYWtvWi8zM3c9PSIsInZhbHVlIjoiNERVU1NhdlEzVzBIbkZ4cmV4Z2JMbHN3NjVrRWZUMzg0OWd1MVd3N1E3ckI5aGhIRVlaa2czWnl4QVdvbjJUSTZxMkhGdlA1ZzA1c0xxU1A0N0hlaS8rZnV4TmxldDVIbHNUZDVNNCtpSS9qb2x3enNodFFITFJGTlZEZVVrN2siLCJtYWMiOiI2MTJmZDcxNzkyM2YwMTM1ZjZkZGRjZTM5YjIzMGFmNTNiNDA1NTAyMmE0OWRhMTBlMzQwMDVjZjY3YmMzNmE3In0%3D',
                    '__cf_bm' : 'MoKFFUtnsCnBMVsc_XiGba.KtzFY_Ta1f6UtGsI_7j4-1731414232-1.0.1.1-0sQuyt.MEHq3govqH2hn5G0QTGypm5VhAs_Bbhx8a1jvPdIz6yUY5HZKXWDlbV8WF2w.FVvnEgBOUdzQ46C3Rw'}

session.cookies.update(cookies)  
start_time = time.perf_counter()
def ScrapFunction(url, headers):
    
    response = session.get(url, headers=headers)
    data = response.json()
    links = ["https://www.immoweb.be/en/classified/" +str(result['property']['type']) + "/for-sale/" + str(result['property']['location']['locality'])+ "/" + str(result['property']['location']['postalCode']) + "/" + str(result['id']) for result in data['results']]
    return links


def getid():
    

    page1 = 0
    page2 = 0
    base_url1 = 'https://www.immoweb.be/fr/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&maxPrice=200000&minPrice=10000&page=' + str(page1) + '&orderBy=relevance'
    base_url2 = 'https://www.immoweb.be/fr/search-results/maison-et-appartement/a-vendre?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&maxPrice=20000000&minPrice=200000&page=' + str(page2) + '&orderBy=relevance'
    
    pages1 = [(base_url1.format(page), headers) for page in range(334)]
    pages2 = [(base_url2.format(page), headers) for page in range(334)]

    with Pool() as pool:
        Links1 = pool.starmap(ScrapFunction, pages1)

        Links2 = pool.starmap(ScrapFunction, pages2) + Links1
        HouseLinks = [link for sub_list in Links2 for link in sub_list]
        
    
    # Export the list into a .csv file
    HouseList = "HouseList.csv"
    with open(HouseList, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["URL"])

        for HouseUrl in HouseLinks:
            writer.writerow([HouseUrl])

        print(f"All houses are encoded into {HouseList}.")
    

if __name__ == '__main__' :
    getid()
execution_time = time.perf_counter()-start_time
print('it took: ' + str(execution_time) + ' to run this script')    
