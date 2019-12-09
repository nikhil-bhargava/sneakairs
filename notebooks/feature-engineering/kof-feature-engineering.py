#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import spacy
import re
pd.set_option('display.max_columns', 50)


# In[8]:


df = context.io.load('KOF_04152019_04')


# In[9]:


df = df.drop(columns='Unnamed: 0')


# In[10]:


df = df.rename(columns = {'Code_Style':'code_style', 'Name':'name', 'Brand':'brand', 'Date':'date',
                    'Retail_Price': 'retail_price', 'Colorway':'colorway', 'Story':'story',
                    'KOF_Wants':'kof_wants', 'Avg_Resale':'avg_resale_stockx'})


# In[11]:


df['retail_price'] = df['retail_price'].astype(int)
df['avg_resale_stockx'] = df['avg_resale_stockx'].str.replace('[^\w\s]','')
df['avg_resale_stockx'] = df['avg_resale_stockx'].astype(int)


# In[12]:


df.head(5)


# ## Merge silhouettes

# In[13]:


all_silhouettes = eval(context.io.load('02_all_silhouettes'))


# In[14]:


temp = []
for i in range(len(all_silhouettes)):
    silhouette = all_silhouettes[i]
    silhouette = silhouette.replace("Nike ", "")
    silhouette = silhouette.replace("Adidas ", "")
    silhouette = silhouette.replace("adidas ", "")
    temp.append(silhouette)
all_silhouettes = temp


# In[15]:


all_silhouettes.append('Air Jordan 1')
all_silhouettes = list(set(all_silhouettes))


# In[16]:


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


# In[18]:


df['silhouette'] = df['name'].apply(lambda x: silhouette_generator(x, all_silhouettes))


# In[19]:


df.head(1)


# ## Create "profitable" feature
# 

# In[7]:


#create columns to calculate net profit
df['price_diff'] = df['avg_resale_stockx'] - df['retail_price']
df['commission_fee'] = abs((df['avg_resale_stockx']) * (9.5/100))
df['seller_fee'] = 5
df['total_credit'] = df['price_diff'] - df['commission_fee'] - df['seller_fee']
df['cashout_fee'] = abs((df['total_credit']) * (2.9/100))
df['net_profit'] = df['total_credit'] - df['cashout_fee']


# In[8]:


#create purchase feature if the net profit is greater than 0
df['profitable'] = np.where(df['net_profit'] > 0, 1, 0)


# In[9]:


#drop columns used to calculate net profit
df.drop(['commission_fee', 'seller_fee', 'total_credit', 'cashout_fee'], axis=1, inplace=True)


# In[10]:


df.head(1)


# ## Create "brand_code" feature

# In[11]:


brand_code = df.groupby('brand').ngroup()
df = pd.concat([df, brand_code], axis=1).rename(columns={0:'brand_code'})


# In[12]:


df.head(1)


# ## Create word2vec color features

# In[13]:


nlp = spacy.load('en_vectors_web_lg')


# In[14]:


def color_word2vec(x, color):
    x = x.lower()
    x = re.sub('[^\w\s]', ' ', x)
    
    token1 = nlp(x)
    token2 = nlp(color)
    
    return token1.similarity(token2)


# In[15]:


df['black'] = df['colorway'].apply(lambda x: color_word2vec(x, "black"))
df['white'] = df['colorway'].apply(lambda x: color_word2vec(x, "white"))
df['brown'] = df['colorway'].apply(lambda x: color_word2vec(x, "brown"))
df['red'] = df['colorway'].apply(lambda x: color_word2vec(x, "red"))
df['blue'] = df['colorway'].apply(lambda x: color_word2vec(x, "blue"))
df['yellow'] = df['colorway'].apply(lambda x: color_word2vec(x, "yellow"))
df['orange'] = df['colorway'].apply(lambda x: color_word2vec(x, "orange"))
df['green'] = df['colorway'].apply(lambda x: color_word2vec(x, "green"))
df['purple'] = df['colorway'].apply(lambda x: color_word2vec(x, "purple"))
df['multi_color'] = df['colorway'].apply(lambda x: color_word2vec(x, "multi color"))


# In[16]:


df['main_color'] = df[['black', 'white', 'red', 'blue', 'yellow',
       'orange', 'green', 'purple', 'multi_color']].idxmax(axis=1)


# In[17]:


df['main_color_id'] = df.groupby('main_color').ngroup()


# In[18]:


df.head(1)


# ## Create "Womens" feature

# In[19]:


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


# In[20]:


df['womens'] = df['name'].apply(lambda x: label_womens(x))


# In[21]:


df.head(1)


# ## Create "bcollab" feature

# In[22]:


def label_bcollab(x):
    name = x
    name = name.lower()
    
    checker1 = ' x ' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[23]:


df['bcollab'] = df['name'].apply(lambda x: label_bcollab(x))


# In[24]:


df.head(1)


# ## Create "OG" feature

# In[25]:


def label_og(x):
    name = x
    name = name.lower()
    
    checker1 = ' og' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[26]:


df['og'] = df['name'].apply(lambda x: label_og(x))


# In[27]:


df.head(1)


# ## Create "SP" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[28]:


def label_sp(x):
    name = x
    name = name.lower()
    
    checker1 = ' sp' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[29]:


df['sp'] = df['name'].apply(lambda x: label_sp(x))


# In[30]:


df.head(1)


# ## Create "QS" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[31]:


def label_qs(x):
    name = x
    name = name.lower()
    
    checker1 = ' qs' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[32]:


df['qs'] = df['name'].apply(lambda x: label_qs(x))


# In[33]:


df.head(1)


# ## Create "SB" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[34]:


def label_sb(x):
    name = x
    name = name.lower()
    
    checker1 = ' sb' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[35]:


df['sb'] = df['name'].apply(lambda x: label_sb(x))


# In[36]:


df.head(1)


# ## Create "LS" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[37]:


def label_ls(x):
    name = x
    name = name.lower()
    
    checker1 = ' ls' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[38]:


df['ls'] = df['name'].apply(lambda x: label_ls(x))


# In[39]:


df.head(1)


# ## Create "NRG" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[40]:


def label_nrg(x):
    name = x
    name = name.lower()
    
    checker1 = ' nrg' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[41]:


df['nrg'] = df['name'].apply(lambda x: label_nrg(x))


# In[42]:


df.head(1)


# ## Create "PRM" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[43]:


def label_prm(x):
    name = x
    name = name.lower()
    
    checker1 = ' prm' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[44]:


df['prm'] = df['name'].apply(lambda x: label_prm(x))


# In[45]:


df.head(1)


# ## Create "NSW" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[46]:


def label_nsw(x):
    name = x
    name = name.lower()
    
    checker1 = ' nsw' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[47]:


df['nsw'] = df['name'].apply(lambda x: label_nsw(x))


# In[48]:


df.head(1)


# ## Create "RETRO" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[49]:


def label_retro(x):
    name = x
    name = name.lower()
    
    checker1 = ' retro' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[50]:


df['retro'] = df['name'].apply(lambda x: label_retro(x))


# In[51]:


df.head(1)


# ## Create "SE" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[52]:


def label_se(x):
    name = x
    name = name.lower()
    
    checker1 = ' se' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[53]:


df['se'] = df['name'].apply(lambda x: label_se(x))


# In[54]:


df.head(1)


# ## Create "PE" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[55]:


def label_pe(x):
    name = x
    name = name.lower()
    
    checker1 = ' pe' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[56]:


df['pe'] = df['name'].apply(lambda x: label_pe(x))


# In[57]:


df.head(1)


# ## Create "GS" feature
# 
# Nike SP represents the highest level of Nike quality, and also an avenue for Nike’s creative endeavors. All NikeLab releases are SP and some collabs are also categorized as SP.
# 
# Example: Nike Free Flyknit Mercurial SP
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/

# In[58]:


def label_gs(x):
    name = x
    name = name.lower()
    
    checker1 = ' gs' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[59]:


df['gs'] = df['name'].apply(lambda x: label_gs(x))


# In[60]:


df.head(1)


# ## Create "HS" feature
# 
# HS – Hyperstrike Shoes labeled HS are the most exclusive of all. They come in very limited quantities, with the majority given to friends and families (FNF) of artists and celebrities. 
# 
# Example: Nike Air Force 1 “Playstation”, which was a promotional shoe given to Sony employees back in 2006.
# 
# https://straatosphere.com/straatopedia-sneaker-terminology-guide/
# 
# ### None were found in this data set. Was skipped for this iteration of the DB.

# In[61]:


def label_hs(x):
    name = x
    name = name.lower()
    
    checker1 = ' hs' in name

    if checker1 == True:
        return 1
    else:
        return 0


# In[62]:


df['hs'] = df['name'].apply(lambda x: label_hs(x))


# In[63]:


df.head(1)


# ## FINAL_DF

# In[64]:


df.head()


# In[65]:


# df.to_csv('KOF_04152019-modelv2.csv', index=False)

