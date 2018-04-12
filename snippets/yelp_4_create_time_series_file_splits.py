# Review file
from datetime import datetime
import pandas as pd

import sys
import os

sys.path.append('../')

import snippets.yelp_constants_columns as cols
import snippets.yelp_constants_file_paths as paths
from snippets import get_logger


def create_time_series_file_splits(df_grouped, output_folder):
    # dict to store metadata
    files = {}

    # write the reviews for each week in a separate file
    for name, group in df_grouped:
        # set the filename
        filename = datetime.strftime(name, '%Y%m%d') + paths.EXT_PKL

        # add it to the metadata store
        files[name] = filename

        # set indexes
        group.reset_index(drop=False, inplace=True)
        group.set_index([cols.DATE, cols.REVIEW_ID], inplace=True)

        # write data
        LOGGER.debug("Writing file: " + filename)
        group.to_pickle(os.path.join(output_folder, filename))

    return files


def store_metadata(metadata, filename):
    files_df = pd.DataFrame.from_dict(metadata, orient='index')
    files_df.index.name = cols.DATE
    files_df.rename(columns={0: 'filename'}, inplace=True)
    files_df.to_pickle(filename)


if __name__ == '__main__':
    """
    This code snippet creates individual files for all the reviews in a month 
    or a week
    """

    # get the logger
    LOGGER = get_logger("snippet_create_time_series_file_splits.out")

    # ------------------------ read the review file --------------------
    LOGGER.debug("Reading the review file.......")
    reviews = pd.read_pickle(paths.PKL_FILE_REVIEW_FILTERED)

    LOGGER.debug("Resetting the index...........")
    reviews.reset_index(drop=False, inplace=True)

    LOGGER.debug("Setting date index............")
    reviews.set_index(cols.DATE, inplace=True)

    # ------------------------ create weekly files --------------------
    LOGGER.debug("Creating weekly files.........")

    # create a weekly grouper
    weekly_reviews = reviews.groupby(pd.Grouper(freq='W'))

    # write the weekly file splits
    metadata = create_time_series_file_splits(weekly_reviews, paths.DIR_FILE_REVIEW_WEEKLY_RAW)

    # store the metadata
    store_metadata(metadata, paths.FILE_REVIEWS_WEEKLY_SUMMARY)

    LOGGER.debug("Weekly files created successfully")

