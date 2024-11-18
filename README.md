# Real Estate Web Scraper

This project is a web scraping tool designed to collect real estate data from [Immoweb](https://www.immoweb.be/). It fetches property listings, extracts relevant details, and compiles the data into a CSV file for further analysis.

## Features

- Scrapes property links from search result pages.
- Extracts detailed information about each property, including:
  - Locality
  - Zip code
  - Property type
  - Price
  - Number of bedrooms
  - Living area
  - Plot surface
  - Number of facades
  - Building condition
  - Availability of amenities (e.g., fireplace, equipped kitchen, garden, terrace, swimming pool).
- Outputs the data as a CSV file for analysis.

## Project Structure
```bash

├── config.json # Contains cookies and headers for requests
├── house_links.csv # List of scraped property links
├── house_data.csv # Final structured property data
├── main.py # Main script to run the scraping workflow
├── utils/
│ ├── get_house_data_scraper.py # Function to scrape individual property data
│ ├── get_links_data_scraper.py # Function to scrape property links from search pages
├── README.md # Project documentation
```
### Main Scripts

1. **`main.py`**:

   - Orchestrates the entire scraping process.
   - Uses multiprocessing for efficiency.
   - Saves scraped links and data to CSV files.

2. **`utils/get_house_data_scraper.py`**:

   - Defines the `get_house_data` function.
   - Scrapes detailed data from individual property pages.

3. **`utils/get_links_data_scraper.py`**:
   - Defines the `get_links_from_page` function.
   - Fetches property links from search results pages.

## Prerequisites

- Python 3.8 or higher
- Dependencies:
  - `requests`
  - `pandas`
  - `bs4` (Beautiful Soup)
  - `multiprocessing`

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the scraper:

```bash
python main.py
```

### 2. Outputs:

• house_links.csv: Contains all property URLs scraped from search results.
• house_data.csv: Contains detailed property data.

## Error Handling

• If a request fails, the script logs the failed URL and HTTP status code.
• If a data field is missing, the corresponding value is set to None.

## Notes

• The config.json file, which contains the necessary cookies and headers for the scraper, is already provided in the repository. Ensure these values remain up to date for successful requests.
• The project uses multiprocessing to speed up the scraping process.
