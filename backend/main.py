from bs4 import BeautifulSoup
import requests
from typing import Union
from fastapi import FastAPI
app = FastAPI()
import re


def parseOldListings(state, suburb_name, postcode, type, street_name, house_number, category, minBeds, maxBeds, baths, cars, sort):
     headers = {
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
     'accept-language': 'en-US,en;q=0.9,mn-MN;q=0.8,mn;q=0.7',
     'cache-control': 'max-age=0',
     'priority': 'u=0, i',
     'referer': 'https://www.oldlistings.com.au/real-estate/NSW/Bella+Vista/2153/buy/1',
     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
     'sec-ch-ua-mobile': '?0',
     'sec-ch-ua-platform': '"macOS"',
     'sec-fetch-dest': 'document',
     'sec-fetch-mode': 'navigate',
     'sec-fetch-site': 'same-origin',
     'sec-fetch-user': '?1',
     'upgrade-insecure-requests': '1',
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
     }
     page = 1
     url = f'https://www.oldlistings.com.au/real-estate/{state}/{suburb_name}/{postcode}/{type}/{page}/'
     if (len(street_name) > 0):
          url = url + street_name
     if (len(category) > 0):
          url = url + f':cat:{category}'
     if (minBeds > 0):
          url = url + f':bed:{minBeds}'
     if (maxBeds > 0):
          url = url + f':bedmax:{maxBeds}'
     if (baths > 0):
          url = url + f':bath:{baths}'
     if (cars > 0):
          url = url + f':car:{cars}'
     if (len(sort) > 0):
          url = url + f':sort:{sort}'
     print(url)
     response = requests.get(url, headers=headers)
     soup = BeautifulSoup(response.text, 'html.parser')
        
     property_divs = soup.find_all('div', class_='property')

     properties = []
    
     for div in property_divs:
          h3_tag = div.find('h3', class_='text-success')
          last_price = div.find('h3', class_='text-success').get_text(strip=True) if h3_tag else None
          historical_prices = []
          h2_tag = div.find('h2', class_='h5')
          address = div.find('h2', class_='h5').get_text(strip=True) if h2_tag else None
          for li in div.select('.mt-3 ul li'):
               date = li.find('small').get_text(strip=True)
               price_text = li.get_text(strip=True).replace(date, '', 1).strip()
               # clean_price = re.search('$(.*) ', price_text)
               # print(clean_price)
               match = re.search(r'\$([^ ]+)', price_text)
               clean_price = price_text
               if match:
                    clean_price = match.group(1)
                    print(clean_price)
               historical_prices.append({'date': date, 'price': clean_price})
          properties.append({"address": address, "last_price": last_price, "historical_prices": historical_prices})

     return properties

def searchSuburbs(suburb_name):
     url = f'https://v0.postcodeapi.com.au/suburbs.json?q={suburb_name}'
     response = requests.get(url)
     data = response.json()
     print(data)
     return data[0]

@app.get("/")
def read_root(suburb_name: str, postcode: str, street_name: str, house_number: str, category: str, minBeds: int, maxBeds: int, baths: int, cars: int, sort: str):
     suburb_data = searchSuburbs(suburb_name)
     if (suburb_data is None):
          return {"error": "Suburb not found", "error_code": 404}
     
     extracted_postcode = suburb_data['postcode']
     if len(postcode) > 1:
          extracted_postcode = postcode
     state = suburb_data['state']['abbreviation']
     suburb_name = suburb_data['name']
     type = 'rent'
     response = parseOldListings(state, suburb_name, extracted_postcode, type, street_name, house_number, category, minBeds, maxBeds, baths, cars, sort)
     return {"message": "success", "data": response}