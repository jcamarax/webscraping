
import os
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import time

import slee

#Open a Chrome webdriver
path = '/Users/jean-charles/PycharmProjects/pythonTestOS/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--enable-javascript")
driver = webdriver.Chrome(path, options=options)


#Url pour trouver tous les apparts sur paris en location, prix par mois < 1500 euros
url2 = 'https://www.seloger.com/list.htm?projects=1&types=1%2C2&places=%5B%7Bcp%3A75%7D%5D&price=NaN%2F1500&enterprise=0&qsVersion=1.0&LISTING-LISTpg=2'


#Creer les URL pour les 20 premieres pages de resultats
url20 = [url2[:-1] + str(i) for i in range(1,21)]

#STEP 2 extract all URL from page

def return_all_ads_frompage(url):
    '''This function returns all the urls from a page containing a list of ads
    Note that all the bellesdemeures ads are removed
    '''
    os.system('protonvpn c -r')
    page = driver.get(url)
    list = BeautifulSoup(driver.page_source)
    test = list.find_all(attrs={"z":1})
    all_adverts = [test['href'] for test in test]
    all_adverts = np.unique(all_adverts)
    mask = [not bool(re.search("belles",all_adverts[i])) for i in range(0, len(all_adverts))]
    all_add_mask = all_adverts[mask]
    return all_add_mask


#Creation of list of French servers
frserv = ['protonvpn c ' + 'FR#' + str(i) for i in range(1,45)]

#Nested function to extract general, a l'interieur, autres sections
def extract_info(tag, section):
    def has_string_gen(tag = tag, section = section):
        return tag.string == section
    return has_string_gen

class soup_data_se_simple:
    def __init__(self, url):
        os.system("sudo protonvpn c -r")
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, features='html.parser')

        self.soup = soup
        self.general = " ".join(self.soup.find(extract_info(soup, section="Général")).parent.parent.strings)
        self.priceblock = " ".join(self.soup.find(attrs={"data-test": "price-block"}).strings)
        self.url = url
        self.location = " ".join(soup.find(id="summary-address").parent.strings)
        self.reference = " ".join(self.soup.find('div',class_ = "SubHeaderstyled__Reference-sc-1s8qndx-7 sWNHa").strings)

        # self.sallebain = re.search("\\d+(?= Salle de bain)", self.general).group(0)
        # self.surface = re.search("\\d+(?=m²)", self.general).group(0)
        # self.rooms = re.search("\\d+(?= (P|p)ièce)", self.general).group(0)
        # self.furnished = bool(re.search("Meublé", self.general))
        # self.toilets = re.search("\\d+(?= Toilette)", self.general).group(0)
        # self.quartier = re.search("\\w+(?= ,)", self.location).group(0)
        # self.arron = re.search("(?<= ,).+", self.location).group(0)
class soup_data:
    def __init__(self, url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
            "Referer": "https://www.scraperapi.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        }
        os.system("sudo protonvpn c -r")
        page = requests.get(url, headers=headers).text
        soup = BeautifulSoup(page, features='html.parser')

        self.soup = soup
        self.general = " ".join(self.soup.find(extract_info(soup, section = "Général")).parent.parent.strings)
        self.description = " ".join(self.soup.find(extract_info(soup, section="L’avis du professionnel")).parent.strings)
        self.priceblock = " ".join(self.soup.find(attrs={"data-test": "price-block"}).strings)
        self.url = url
        self.reference = " ".join(self.soup.find('div',class_ = "SubHeaderstyled__Reference-sc-1s8qndx-7 sWNHa").strings)
        self.location = " ".join(self.soup.find(id="summary-address").parent.strings)
        self.date_scrape = datetime.today().strftime('%d-%m-%Y')

master = []
errors = {}

#Creation of loop
for j in range(2):
    return_all_ads_frompage(url20[j])
    for i in range(3):
        time.sleep(np.random.random(3)[1])
        try:
            master.append(soup_data(all_add_mask[i]))
        except:
            errors[str(i)] = all_add_mask[i]

