# Review file
import pandas as pd
from datetime import datetime

import sys
import os

sys.path.append('../')

import snippets.amazon_constants_file_paths as paths

if __name__ == '__main__':
    """
    This code snippet constructs the amazon data stream
    """

    folder = paths.DIR_AMAZON

    # ------------------------ read the product categories --------------------
    print("Read the beauty dataset")
    beauty = pd.read_pickle(os.path.join(folder, "reviews_Beauty_5.pkl.gzip"))

    print("Read the cell phone and accessories dataset")
    phones = pd.read_pickle(os.path.join(folder, "reviews_Cell_Phones_and_Accessories_5.pkl.gzip"))

    print("Read the clothing, shoes and jewelry dataset")
    clothing = pd.read_pickle(os.path.join(folder, "reviews_Clothing_Shoes_and_Jewelry_5.pkl.gzip"))

    print("Read the electronics dataset")
    electronics = pd.read_pickle(os.path.join(folder, "reviews_Electronics_5.pkl.gzip"))

    print("Read the home and kitchen dataset")
    home = pd.read_pickle(os.path.join(folder, "reviews_Home_and_Kitchen_5.pkl.gzip"))

    print("Read the apps for android dataset")
    apps = pd.read_pickle(os.path.join(folder, "reviews_Apps_for_Android_5.pkl.gzip"))

    print("Read the cds and vinyl dataset")
    cds = pd.read_pickle(os.path.join(folder, "reviews_CDs_and_Vinyl_5.pkl.gzip"))

    print("Read the health and personal care dataset")
    health = pd.read_pickle(os.path.join(folder, "reviews_Health_and_Personal_Care_5.pkl.gzip"))

    print("Read the kindle store dataset")
    kindle = pd.read_pickle(os.path.join(folder, "reviews_Kindle_Store_5.pkl.gzip"))

    # ------------------------ construct data stream ----------------------------
    data = pd.concat([beauty, phones, clothing, electronics, home, apps, cds, health, kindle])

    data.reset_index(inplace=True, drop=False)
    data.set_index("date", inplace=True)
    data.sort_index(inplace=True)

    # considering data only from 2011
    data = data.loc["2011":, :]

    # setting the categories to be chosen for each quarter in the year
    product_categories = {
        datetime(2011, 1, 31): ['home and kitchen', 'health and personal care', 'cell phones and accessories'],
        datetime(2011, 4, 30): ['kindle store', 'home and kitchen', 'apps for android'],
        datetime(2011, 7, 31): ['home and kitchen', 'electronics', 'clothing, shoes and jewelry'],
        datetime(2011, 10, 31): ['home and kitchen', 'kindle store', 'cds and vinyl'],
        datetime(2012, 1, 31): ['cds and vinyl', 'cell phones and accessories', 'home and kitchen'],
        datetime(2012, 4, 30): ['electronics', 'health and personal care', 'apps for android'],
        datetime(2012, 7, 31): ['cds and vinyl', 'kindle store', 'health and personal care'],
        datetime(2012, 10, 31): ['cell phones and accessories', 'health and personal care',
                                 'clothing, shoes and jewelry'],
        datetime(2013, 1, 31): ['apps for android', 'kindle store', 'electronics'],
        datetime(2013, 4, 30): ['electronics', 'cell phones and accessories', 'cds and vinyl'],
        datetime(2013, 7, 31): ['cell phones and accessories', 'home and kitchen', 'cds and vinyl'],
        datetime(2013, 10, 31): ['cds and vinyl', 'kindle store', 'cell phones and accessories'],
        datetime(2014, 1, 31): ['clothing, shoes and jewelry', 'beauty', 'cell phones and accessories'],
        datetime(2014, 4, 30): ['health and personal care', 'apps for android', 'home and kitchen'],
        datetime(2014, 7, 31): ['home and kitchen', 'cell phones and accessories', 'cds and vinyl']
    }

    # create three month groups
    grouped = data.groupby(pd.Grouper(freq='3M'))

    filtered_data = []
    for name, group in grouped:
        # get the categories
        categories = group.loc[:, "category"].unique()

        # randomly select 3 categories
        selected = product_categories[name]

        # filter for selected categories
        selected_data = group[group['category'].isin(selected)]

        # add to result list
        filtered_data.append(selected_data)

    filtered_data = pd.concat(filtered_data)

    # remove duplicates
    filtered_data = filtered_data.reset_index(drop=False).drop_duplicates(["date", "review_id"]).set_index(
        ["date", "review_id"])

    # save
    filtered_data.reset_index(drop=False, inplace=True)
    filtered_data.set_index(["date", "review_id"], inplace=True)
    filtered_data.sort_index(inplace=True)
    filtered_data.to_pickle(os.path.join(folder, "filtered", "reviews.pkl.gzip"))
