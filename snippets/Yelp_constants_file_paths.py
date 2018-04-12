import os

# extensions
EXT_CSV = ".csv"
EXT_PKL = ".pkl.gzip"
EXT_JSON = ".json"

# name of the files
FILE_NAME_REVIEW = "review"

# file paths
DIR_YELP = "../data/yelp"

DIR_CSV = "{0}/csv".format(DIR_YELP)
DIR_JSON = "{0}/json".format(DIR_YELP)
DIR_LANG = "{0}/lang".format(DIR_YELP)
DIR_FILTERED = "{0}/filtered".format(DIR_YELP)

# The yelp files in CSV format
JSON_FILE_REVIEW = "{0}/{1}{2}".format(DIR_JSON, FILE_NAME_REVIEW, EXT_JSON)

# The yelp files in CSV format
CSV_FILE_REVIEW = "{0}/{1}{2}".format(DIR_CSV, FILE_NAME_REVIEW, EXT_CSV)

# The yelp review files annotated with the language of the text
CSV_FILE_REVIEW_ALL_LANG = "{0}/{1}{2}".format(DIR_LANG, FILE_NAME_REVIEW, EXT_CSV)
PKL_FILE_REVIEW_ALL_LANG = "{0}/{1}{2}".format(DIR_LANG, FILE_NAME_REVIEW, EXT_PKL)

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
