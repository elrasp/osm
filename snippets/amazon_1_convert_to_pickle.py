# Review file
import pandas as pd
import gzip

import sys
import os

sys.path.append('../')

import snippets.amazon_constants_file_paths as paths


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)


def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def convert_to_pkl(filename: str, category: str):
    df = getDF(os.path.join(paths.DIR_AMAZON, filename + '.json.gz'))
    df.drop(["reviewTime", "reviewerName", "helpful", "summary"], axis=1, inplace=True)
    df["category"] = category

    df["review_id"] = df["reviewerID"]
    df["review_id"] = df["review_id"] + "_"
    df["review_id"] = df["review_id"] + df["asin"]
    df.drop(["reviewerID", "asin"], axis=1, inplace=True)

    df.rename(columns={"reviewText": "text", "overall": "stars", "unixReviewTime": "date"}, inplace=True)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df.set_index(["date", "review_id"], inplace=True)

    df.sort_index(inplace=True)
    df.to_pickle(os.path.join(paths.DIR_AMAZON, filename + ".pkl.gzip"))


if __name__ == '__main__':
    """
    This code snippet reads the amazon dataset files and converts it to readable pickles
    """

    # ------------------------ read the review file --------------------
    print("Converting Beauty dataset")
    convert_to_pkl("reviews_Beauty_5", 'beauty')

    print("Converting cell phones and accessories dataset")
    convert_to_pkl("reviews_Cell_Phones_and_Accessories_5", 'cell phones and accessories')

    print("Converting clothing, shoes and jewelry dataset")
    convert_to_pkl("reviews_Clothing_Shoes_and_Jewelry_5", 'clothing, shoes and jewelry')

    print("Converting electronics dataset")
    convert_to_pkl("reviews_Electronics_5", 'electronics')

    print("Converting homes and kitchen dataset")
    convert_to_pkl("reviews_Home_and_Kitchen_5", 'home and kitchen')

    print("Converting apps for android dataset")
    convert_to_pkl("reviews_Apps_for_Android_5", 'apps for android')

    print("Converting cds and vinyls dataset")
    convert_to_pkl("reviews_CDs_and_Vinyl_5", 'cds and vinyl')

    print("Converting health and personal care dataset")
    convert_to_pkl("reviews_Health_and_Personal_Care_5", 'health and personal care')

    print("Converting kindle store dataset")
    convert_to_pkl("reviews_Kindle_Store_5", 'kindle store')


