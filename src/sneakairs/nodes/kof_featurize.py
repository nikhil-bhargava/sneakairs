import pandas as pd
import numpy as np
import spacy
import re
from sneakairs.nodes.kof_functions import silhouette_generator, color_word2vec, label_womens, label_bcollab, label_og, label_sp, label_qs, label_sb, label_ls, label_nrg, label_prm, label_nsw, label_retro, label_se, label_pe, label_gs, label_hs

def featurize_kof(*args):

    """Cleans scraped KOF data.

    Args:
        df: Ingest a csv file containing scraped KOF data.

    Returns:
        df: A cleaned version of scraped KOF data.

    """

    df = args[0]

    # initial cleaning & changes to df
    df = df.drop(columns='Unnamed: 0')
    df = df.rename(columns = {'Code_Style':'code_style', 'Name':'name', 'Brand':'brand', 'Date':'date',
                    'Retail_Price': 'retail_price', 'Colorway':'colorway', 'Story':'story',
                    'KOF_Wants':'kof_wants', 'Avg_Resale':'avg_resale_stockx'})
    df['retail_price'] = df['retail_price'].astype(int)
    df['avg_resale_stockx'] = df['avg_resale_stockx'].str.replace('[^\w\s]','')
    df['avg_resale_stockx'] = df['avg_resale_stockx'].astype(int)

    # feature 1: merge silhouettes
    all_silhouettes = eval(args[1])
    # strip out brand name from silhouette name
    temp = []
    for i in range(len(all_silhouettes)):
        silhouette = all_silhouettes[i]
        silhouette = silhouette.replace("Nike ", "")
        silhouette = silhouette.replace("Adidas ", "")
        silhouette = silhouette.replace("adidas ", "")
        temp.append(silhouette)
    all_silhouettes = temp
    all_silhouettes.append('Air Jordan 1')
    all_silhouettes = list(set(all_silhouettes))
    df['silhouette'] = df['name'].apply(lambda x: silhouette_generator(x, all_silhouettes))

    #feature 2: profitable
    #create columns to calculate net profit
    df['price_diff'] = df['avg_resale_stockx'] - df['retail_price']
    df['commission_fee'] = abs((df['avg_resale_stockx']) * (9.5/100))
    df['seller_fee'] = 5
    df['total_credit'] = df['price_diff'] - df['commission_fee'] - df['seller_fee']
    df['cashout_fee'] = abs((df['total_credit']) * (2.9/100))
    df['net_profit'] = df['total_credit'] - df['cashout_fee']
    #create purchase feature if the net profit is greater than 0
    df['profitable'] = np.where(df['net_profit'] > 0, 1, 0)
    #drop columns used to calculate net profit
    df.drop(['commission_fee', 'seller_fee', 'total_credit', 'cashout_fee'], axis=1, inplace=True)

    #feature 3: brand code
    brand_code = df.groupby('brand').ngroup()
    df = pd.concat([df, brand_code], axis=1).rename(columns={0:'brand_code'})

    #feature 4: word2vec colors
    nlp = spacy.load('en_vectors_web_lg')
    df['black'] = df['colorway'].apply(lambda x: color_word2vec(x, "black", nlp))
    df['white'] = df['colorway'].apply(lambda x: color_word2vec(x, "white", nlp))
    df['brown'] = df['colorway'].apply(lambda x: color_word2vec(x, "brown", nlp))
    df['red'] = df['colorway'].apply(lambda x: color_word2vec(x, "red", nlp))
    df['blue'] = df['colorway'].apply(lambda x: color_word2vec(x, "blue", nlp))
    df['yellow'] = df['colorway'].apply(lambda x: color_word2vec(x, "yellow", nlp))
    df['orange'] = df['colorway'].apply(lambda x: color_word2vec(x, "orange", nlp))
    df['green'] = df['colorway'].apply(lambda x: color_word2vec(x, "green", nlp))
    df['purple'] = df['colorway'].apply(lambda x: color_word2vec(x, "purple", nlp))
    df['multi_color'] = df['colorway'].apply(lambda x: color_word2vec(x, "multi color", nlp))
    df['main_color'] = df[['black', 'white', 'brown', 'red', 'blue', 'yellow',
       'orange', 'green', 'purple', 'multi_color']].idxmax(axis=1)
    df['main_color_id'] = df.groupby('main_color').ngroup()

    #boolean features
    df['womens'] = df['name'].apply(lambda x: label_womens(x))

    df['bcollab'] = df['name'].apply(lambda x: label_bcollab(x))

    df['og'] = df['name'].apply(lambda x: label_og(x))

    df['sp'] = df['name'].apply(lambda x: label_sp(x))

    df['qs'] = df['name'].apply(lambda x: label_qs(x))

    df['sb'] = df['name'].apply(lambda x: label_sb(x))

    df['ls'] = df['name'].apply(lambda x: label_ls(x))

    df['nrg'] = df['name'].apply(lambda x: label_nrg(x))

    df['prm'] = df['name'].apply(lambda x: label_prm(x))

    df['nsw'] = df['name'].apply(lambda x: label_nsw(x))

    df['retro'] = df['name'].apply(lambda x: label_retro(x))

    df['se'] = df['name'].apply(lambda x: label_se(x))

    df['pe'] = df['name'].apply(lambda x: label_pe(x))

    df['gs'] = df['name'].apply(lambda x: label_gs(x))

    df['hs'] = df['name'].apply(lambda x: label_hs(x))

    return df

