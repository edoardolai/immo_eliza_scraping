from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
def get_links_from_page(driver, page):
    links = list()
    driver.get(page)
    for link in driver.find_elements(By.XPATH, "//a[contains(@href, '/en/classified/')]"):
            links.extend(link.get_attribute("href") + '\n')