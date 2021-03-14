#Load packages
import pickle5 as pickle
import os
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import time
import numpy as np


#Load class soup_data
class soup_data:
    '''
    The soup_data is a class object containing the content of one advert scrapped. The attribute contains information  about specific information from the advert. When inititating the class object on the url, the class will make a HTTP request, parse the HTTP with beautiful soup lib.
    @soup: beautiful soup object
    @general:  text  describing the general info of the advert
    @priceblock: text containing different prices related to the advert
    @url: the url of the adv
    @reference: the unique identifier of the advert
    @location: text containing information of the location 
    @date_scrap: the date when the advert was scraped

    '''
    def __init__(self, url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
            "Referer": "https://www.scraperapi.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        }
        #CLI command to switch VPN server
        os.system("sudo protonvpn c -r")
        #HTTP request
        page = requests.get(url, headers=headers).text
        #Parser with beautiful soup
        soup = BeautifulSoup(page, features='html.parser')

        #Attributes
        self.soup = soup
        self.general = " ".join(self.soup.find(extract_info(soup, section="Général")).parent.parent.strings)
        self.description = " ".join(
            self.soup.find(extract_info(soup, section="L’avis du professionnel")).parent.strings)
        self.priceblock = " ".join(self.soup.find(attrs={"data-test": "price-block"}).strings)
        self.url = url
        self.reference = " ".join(self.soup.find('div', class_="SubHeaderstyled__Reference-sc-1s8qndx-7 sWNHa").strings)
        self.location = " ".join(self.soup.find(id="summary-address").parent.strings)
        self.date_scrape = datetime.today().strftime('%d-%m-%Y')

def extract(param, text):
    '''Function to return a specific number of units (number of bathrooms, rooms) in the soup_data.general
    Parameters:
        param: regex to to find
        text: text to scrap in this instance soup_data.general
    Examples:
    for number of roooms param = "pièce"
    for number of toilets param = "toilette"
    '''
    info = re.search("(\d*,?\d+) ?(?="+param+")", text.lower())
    try:
        return re.sub(",",".",info.group(1))
    except:
        return "NaN"
      
def price(param, text):
    '''Function to return a specific fee in the soup_data.priceblock
    Parameters:
        param: regex to find
        text: text to scrap in soup_data.priceblock
        
    Examples:
    for rent param = "le loyer mensuel"
    for deposit param = "dépôt"
    for agency fees param = "à la charge"
    '''
    fees = re.search(param+".+?(\d+,?\d+)",text.lower())
    try:
        return re.sub(",",".",fees.group(1)) #RE to make sure the decimal operator are point.
    except:
        return "NaN"

def specific(param,text):
    '''Function to return True if the word param is in the soup_data.general
    Parameters:
        param: regex to find
        text: text to scrap in soup_data.general
        
    Examples:
    for meublé param = "meublé"
    '''
    info = re.search(param,text)
    return bool(info)

def location(text):
    '''Function that returns the name of the neighbourhood  and the arrondissement in the soup_data.location
        Parameters:
            text: text to scrap in soup_data.location
   
    '''
    match = re.search("quartier\s+(.+)\s+?,.*?(\d+)",text.lower())
    try:
        quartier =  match.group(1)
        arrond = re.sub(",",".",match.group(2))
        return (quartier, int(arrond))
    except:
        return ("NaN", int(np.nan))