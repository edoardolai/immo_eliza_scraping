def get_links_from_page(url, session):
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            base_url = "https://www.immoweb.be/en/classified/{}/for-sale/{}/{}/{}/"
            links = [base_url.format(str(result['property']['subtype']) ,str(result['property']['location']['district']),str(result['property']['location']['postalCode']),str(result["id"] )) for result in data['results']]
            return links
        else:
            print(f"Failed to fetch {url}: {response.status_code}")


