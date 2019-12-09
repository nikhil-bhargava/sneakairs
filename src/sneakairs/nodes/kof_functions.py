import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import spacy

def p_get_data(number):
    data = soup.findAll('p')[number].contents[0]
    return data

def meta_get_data(number):
    data = soup.findAll('meta')[number]['content']
    return data

def silhouette_generator(name, silhouettes):    
    matches = []
    for x in silhouettes:
        if x in name and x not in matches:
            matches.append(x)
        
    try:
        silhouette = max(matches, key=len)
    except:
        silhouette = np.nan
        
    return silhouette

def color_word2vec(x, color, nlp):
    x = x.lower()
    x = re.sub('[^\w\s]', ' ', x)
    
    token1 = nlp(x)
    token2 = nlp(color)
    
    return token1.similarity(token2)

def label_womens(x):
    name = x
    name = name.lower()
    
    checker1 = 'wmns' in name
    checker2 = 'womens' in name
    checker3 = "women's" in name

    if checker1 == True or checker2 == True or checker3 == True:
        return 1
    else:
        return 0

def label_bcollab(x):
    name = x
    name = name.lower()
    
    checker1 = ' x ' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_og(x):
    name = x
    name = name.lower()
    
    checker1 = ' og' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_sp(x):
    name = x
    name = name.lower()
    
    checker1 = ' sp' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_qs(x):
    name = x
    name = name.lower()
    
    checker1 = ' qs' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_sb(x):
    name = x
    name = name.lower()
    
    checker1 = ' sb' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_ls(x):
    name = x
    name = name.lower()
    
    checker1 = ' ls' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_nrg(x):
    name = x
    name = name.lower()
    
    checker1 = ' nrg' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_prm(x):
    name = x
    name = name.lower()
    
    checker1 = ' prm' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_nsw(x):
    name = x
    name = name.lower()
    
    checker1 = ' nsw' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_retro(x):
    name = x
    name = name.lower()
    
    checker1 = ' retro' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_se(x):
    name = x
    name = name.lower()
    
    checker1 = ' se' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_pe(x):
    name = x
    name = name.lower()
    
    checker1 = ' pe' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_gs(x):
    name = x
    name = name.lower()
    
    checker1 = ' gs' in name

    if checker1 == True:
        return 1
    else:
        return 0

def label_hs(x):
    name = x
    name = name.lower()
    
    checker1 = ' hs' in name

    if checker1 == True:
        return 1
    else:
        return 0
