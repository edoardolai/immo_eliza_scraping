#ImmowebScraper

# Importation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


from dotenv import load_dotenv
import os
load_dotenv()
# Make selenium and Firefox work together (On my Ubuntu)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.set_preference("permissions.default.image", 2)  # 2 pour bloquer le chargement des images
options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")  # Désactiver Flash si nécessaire
geckodriver_path = "/snap/bin/geckodriver"
driver_service = Service(executable_path=geckodriver_path)


driver = webdriver.Firefox(options=options, service=driver_service)

    

def GetImmoLinks():
    # Opens Moodle
    driver.get('https://www.immoweb.be/fr')
    driver.implicitly_wait(10)

    try :
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-dcJsrY:nth-child(2)"))).click()
        print('yes cookies')
    except:
        driver.execute_script('UC_UI.denyAllConsents().then(UC_UI.closeCMP);')
        print('no cookies')

    try : 
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(By.CSS_SELECTOR,'.notification-banner__close-icon')).click() 
    except :
        print('couldnt close up banner')   

    

    # ConnectWithAnAccount
   
    driver.implicitly_wait(5)
    ConnectionButton = driver.find_element(By.ID, 'myImmowebMenu')
    ConnectionButton.click()
    LoginField = driver.find_element(By.NAME, 'login-email')
    PasswordField = driver.find_element(By.NAME, "login-password")
    LoginButton = driver.find_element(By.CSS_SELECTOR, 'div.field:nth-child(4) > button:nth-child(1)')


    LoginField.send_keys('33j6ahq30@mozmail.com')
    password=os.getenv('PASSWORDimmoweb')
    PasswordField.send_keys(password)  
    LoginButton.click()
    HouseLinks =[]
    for page in range (1,334) :
        driver.get('https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&minPrice=10000&priceType=SALE_PRICE&page=' + str(page) + '&orderBy=cheapest')
        PageLinks = driver.find_elements(By.XPATH, "//a[contains(@href, '/fr/annonce/')]")
        HouseLinks.extend([link.get_attribute("href") for link in PageLinks])
        driver.implicitly_wait(1)
        

   

    # Afficher les liens"
    HouseList = "HouseList.csv"
    with open(HouseList, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Houses", "URL"])  # En-têtes du fichier CSV
        writer.writerows(HouseLinks)  # Écrit toutes les lignes de la liste

    print(f"Les données ont été exportées dans {filename}.")

    for url in HouseLinks:
        print(url)

GetImmoLinks()