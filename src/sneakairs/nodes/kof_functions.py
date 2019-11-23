import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def p_get_data(number):
    data = soup.findAll('p')[number].contents[0]
    return data

def meta_get_data(number):
    data = soup.findAll('meta')[number]['content']
    return data