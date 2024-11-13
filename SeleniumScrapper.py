from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
import numpy as np
import re
import json

def get_links_from_page(page):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_preference("permissions.default.image", 2)
    options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

    driver = webdriver.Firefox(options=options)
    links = []
    try:
        driver.get(page)
        for link in driver.find_elements(By.XPATH, "//a[contains(@href, '/en/classified/')]"):
            if(re.match(r'.*project.*',link.get_attribute("href")) == None):
                links.append(link.get_attribute("href") + '\n')
    finally:
        driver.quit()
    
    return links

if __name__ == '__main__':
    base_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={}&orderBy=relevance'
    pages = [base_url.format(page) for page in range(192)]

    with Pool() as pool: 
        all_links = pool.map(get_links_from_page, pages)

    # with open('test.json', mode='w', encoding='utf-8') as file:
    #         json.dump(all_links, file, ensure_ascii=False, indent=4)
    
    # Flatten the list of lists
    #  element for row in matrix for element in row if element
    flat_links = [link for sub_list in all_links for link in sub_list] #todo fix this not flattening...

    # Save to file
    with open('test.csv', mode='w') as file:
        file.writelines(flat_links)
