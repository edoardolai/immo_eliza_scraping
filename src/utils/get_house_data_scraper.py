import re
from bs4 import BeautifulSoup as bs
import urllib.parse


def get_house_data(url: str, session, headers):
    response = session.get(url, headers=headers)
    house_dict= dict()
    if response.status_code == 200:
        house_page = bs(response.content, 'html.parser')
        data = response.json()
        data['results']
        cleaned_url = re.sub(r"[^\w\s()\u00C0-\u017F-]/+|[\s']*",'',urllib.parse.unquote(url))
        re.findall(r'for-sale/(\w+([-\w*])*)', urllib.parse.unquote(cleaned_url))
        locality_match = re.findall(r'for-sale/(\w+([-\w*])*)', cleaned_url)
        #Not all links have these properties so sometimes an empty list is returned, causing an out of range index error
        house_dict['locality'] = locality_match[0][0].title() if locality_match else None
        zip_match = re.findall(r'/(\d{4})/', cleaned_url)
        house_dict['zip_code'] = zip_match[0].title() if zip_match else None
        property_type_match = re.findall(r'(classified)/(\w+[_\w*]*)', cleaned_url)
        house_dict['property_type'] = property_type_match[0][1].title() if property_type_match else None
        price = house_page.select_one('.classified__price .sr-only').get_text().strip('€')
        house_dict['price'] = price if price != '' else None
        house_dict['nb_bedrooms'] = extract_table_data(house_page, r'Bedrooms')
        house_dict['living_area'] = extract_table_data(house_page, r'Living\sarea')
        house_dict['surface_of_the_plot'] = extract_table_data(house_page, r'Surface\sof\sthe\splot')
        house_dict['nb_facades'] = extract_table_data(house_page, r'Number\sof\sfrontages')
        house_dict['state_of_building'] = extract_table_data(house_page, r'Building\scondition')
        fireplace = extract_table_data(house_page,r"How\smany\sfireplaces")
        fireplace = 1 if fireplace is not None and int(fireplace) > 0 else 0;
        house_dict['fireplace'] = fireplace
        kitchen_type = extract_table_data(house_page, r"Kitchen\stype") 
        kitchen_type_list = ['Installed', 'Hyper equipped','USA installed','USA hyper equipped']
        kitchen_type = 1 if kitchen_type in kitchen_type_list else 0
        house_dict['Equipped kitchen'] = kitchen_type
        garden_surface = extract_table_data(house_page, r"Garden\ssurface")
        garden, garden_surface = (0, 0)if garden_surface is None else (1, garden_surface)
        house_dict['Garden'] = garden
        house_dict['Garden surface'] = garden_surface
        terrace_surface = extract_table_data(house_page,r"Terrace\ssurface")
        terrace, terrace_surface = (0, None) if terrace_surface is None else (1, terrace_surface)
        house_dict['Terrace'] = terrace
        house_dict['Terrace surface'] = garden_surface
        furnished = extract_table_data(house_page, r"Furnished")
        furnished = 1 if furnished == 'Yes' else 0
        house_dict['Furnished'] = furnished
        swimming_pool = extract_table_data(house_page, r"Swimming\spool")
        swimming_pool = 1 if swimming_pool == "Yes" else 0
        house_dict['Swimming pool'] = swimming_pool
        return house_dict
    else:
        print(f"Failed to fetch {url}: {response.status_code}")

def extract_table_data(page, regex):
    searched_tag = page.find('th',string = re.compile(regex))
    if searched_tag is not None:
        return page.find('th',string = re.compile(regex)).next_sibling.next_element.next_element.strip()
    else:
        return None