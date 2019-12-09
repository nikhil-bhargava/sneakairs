import pandas as pd
import numpy as np

def clean_kof(df):

    """Cleans scraped KOF data.

    Args:
        df: Ingest a csv file containing scraped KOF data.

    Returns:
        df: A cleaned version of scraped KOF data.

    """

    # rename all columns to lowercase
    df = df.rename(columns = {'Code_Style':'code_style', 'Name':'name', 'Brand':'brand', 'Date':'date',
                        'Retail_Price': 'retail_price', 'Colorway':'colorway', 'Story':'story',
                        'KOF_Wants':'kof_wants'})

    # code style is a unique identifier. can't have this value as null
    df = df[~df['code_style'].isnull()]

    return df
