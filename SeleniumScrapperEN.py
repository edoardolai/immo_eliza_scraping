#ImmowebScraper

# Importation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import random

# Make selenium and Firefox work together (On my Ubuntu)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

#set options to block images and flash animations #gottagofast   
options.set_preference("permissions.default.image", 2)
options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

geckodriver_path = "/snap/bin/geckodriver"

driver_service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(options=options, service=driver_service)



def GetImmoLinks():
    # Opens Immoweb
    driver.get('https://www.immoweb.be/fr')
    driver.implicitly_wait(10)

    #Free yourself from cookie slavery
    try :
        driver.implicitly_wait(10)
        driver.execute_script('UC_UI.denyAllConsents().then(UC_UI.closeCMP);')
        print('no cookies')
    except:
        
        print('Cookies got us...')


    # Connect to immoweb with  an account, to avoid restriction to no sub visitors
   
    driver.implicitly_wait(5) # Waits for cookies to go away
    ConnectionButton = driver.find_element(By.ID, 'myImmowebMenu')
    ConnectionButton.click()
    LoginField = driver.find_element(By.NAME, 'login-email')
    PasswordField = driver.find_element(By.NAME, "login-password")
    LoginButton = driver.find_element(By.CSS_SELECTOR, 'div.field:nth-child(4) > button:nth-child(1)')
    LoginField.send_keys('33j6ahq30@mozmail.com')
    password='6&_STDM;N2:i99u'
    PasswordField.send_keys(password)  
    LoginButton.click()
    #Free yourself from cookie slavery if first time didnt work
    try :
        driver.implicitly_wait(10)
        driver.execute_script('UC_UI.denyAllConsents().then(UC_UI.closeCMP);')
        print('Nice try, no cookies on my watch')
    except:
        
        print('Cookies got us again...')

    #Create a list of all houses and appartments starting from 10K € 
    HouseLinks =[]
    for page in range (1,334) :  #list 333 pages cause i had that many but it could be improved to the actual number at time given
        driver.get('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=10000&page='+str(page)+'&orderBy=relevance')
        PageLinks = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/classified')]")
        HouseLinks.extend([link.get_attribute("href") for link in PageLinks])
        driver.implicitly_wait(1) # wait a second between pages to stay undercover and dodge internet police
        

   

    # Export the list into a .csv file
    HouseList = "HouseList.csv"
    with open(HouseList, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Houses", "URL"])  # En-têtes du fichier CSV
        writer.writerows(HouseLinks)  # Écrit toutes les lignes de la liste

    print(f"All houses are encoded into {HouseList}.")


GetImmoLinks()