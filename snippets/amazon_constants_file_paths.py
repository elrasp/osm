import os

# extensions
EXT_CSV = ".csv"
EXT_PKL = ".pkl.gzip"
EXT_JSON = ".json"

# name of the files
FILE_NAME_REVIEW = "review"

# file paths
DIR_AMAZON = "../data/amazon"

DIR_FILTERED = "{0}/filtered".format(DIR_AMAZON)

# The review file containing reviews only in english and length above the threshold
PKL_FILE_REVIEW_FILTERED = "{0}/{1}{2}".format(DIR_FILTERED, FILE_NAME_REVIEW, EXT_PKL)

# weekly review file paths
DIR_WEEKLY = "weekly"
DIR_RAW = "raw"
DIR_PRE_PROCESSED = "preprocessed"
DIR_RESULTS = "results"
DIR_FILE_REVIEW_WEEKLY = os.path.join(DIR_FILTERED, DIR_WEEKLY)
DIR_FILE_REVIEW_WEEKLY_RAW = os.path.join(DIR_FILE_REVIEW_WEEKLY, DIR_RAW)

# weekly summmary file
FILE_REVIEWS_WEEKLY_SUMMARY = os.path.join(DIR_FILE_REVIEW_WEEKLY, "summary" + EXT_PKL)


