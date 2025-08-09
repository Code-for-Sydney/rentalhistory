from bs4 import BeautifulSoup
import requests
from typing import Union
from fastapi import FastAPI
app = FastAPI()


def parseOldListings(url):
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
     response = requests.get(url, headers=headers)
     soup = BeautifulSoup(response.text, 'html.parser')
        
     property_divs = soup.find_all('div', class_='property')

     properties = []
    
     for div in property_divs:
          last_price = soup.find('h3', class_='text-success').get_text(strip=True)
          historical_prices = []
          address = soup.find('h2', class_='h5').get_text(strip=True)
          for li in soup.select('.mt-3 ul li'):
               date = li.find('small').get_text(strip=True)
               price_text = li.get_text(strip=True).replace(date, '', 1).strip()
               historical_prices.append({'date': date, 'price': price_text})
          properties.append({"address": address, "last_price": last_price, "historical_prices": historical_prices})

     return properties


# https://v0.postcodeapi.com.au/suburbs.json?q=Milsons%20point

def searchSuburbs(suburb_name):
     url = f'https://v0.postcodeapi.com.au/suburbs.json?q={suburb_name}'
     response = requests.get(url)
     data = response.json()
     return data[0]

@app.get("/")
def read_root(suburb_name: str):
     suburb_data = searchSuburbs(suburb_name)
     print(suburb_data)
     postcode = suburb_data['postcode']
     state = suburb_data['state']['abbreviation']
     suburb_name = suburb_data['name']
     type = 'buy'
     url = f'https://www.oldlistings.com.au/real-estate/{state}/{suburb_name}/{postcode}/{type}/'
     print(url)
     response = parseOldListings(url)
     return response