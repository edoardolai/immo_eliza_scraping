from bs4 import BeautifulSoup
import requests
import re


house_page = BeautifulSoup(open("test_page.html"), "html.parser")
house_dict = []

# Duplicated function
def extract_table_data(page, regex):
    searched_tag = page.find('th',string = re.compile(regex))
    if searched_tag is not None:
        return page.find('th',string = re.compile(regex)).next_sibling.next_element.next_element.strip()
    else:
        return None

# fireplace  
fireplace = extract_table_data(house_page,r"How\smany\sfireplaces")
fireplace = int(fireplace)
if fireplace > 0:
    fireplace = 1
else:
    fireplace = 0

house_dict['fireplace'] = fireplace

# Kitchen type
kitchen_type = extract_table_data(house_page, r"Kitchen\stype") 
print(kitchen_type)
if (kitchen_type == "Installed") or (kitchen_type == "Hyper equipped") or (kitchen_type == "USA installed") or (kitchen_type == "USA hyper equipped"):
    kitchen_type = 1
elif kitchen_type == "Undefined":
    kitchen_type = None
else:
    kitchen_type = 0 
print("kitchen_type", kitchen_type)

house_dict['Equipped kitchen'] = kitchen_type

# Garden
garden_surface = extract_table_data(house_page, r"Garden\ssurface")
if garden_surface is None:
    garden = 0
    garden_surface = None
else:
    garden = 1

house_dict['Garden'] = garden
house_dict['Garden surface'] = garden_surface


# Terrace
terrace_surface = extract_table_data(house_page,r"Terrace\ssurface")
if terrace_surface is None:
    terrace = 0
    terrace_surface = None
else:
    terrace = 1

house_dict['Terrace'] = garden
house_dict['Terrace surface'] = garden_surface

# furnished
furnished = extract_table_data(house_page, r"Furnished")
if furnished == "Yes":
    furnished = 1
else:
    furnished = 0
house_dict['Furnished'] = garden


# swimming_pool
swimming_pool = extract_table_data(house_page, r"Swimming\spool")
if swimming_pool == "Yes":
    swimming_pool = 1
else:
    swimming_pool = 0

house_dict['Swimming pool'] = swimming_pool


