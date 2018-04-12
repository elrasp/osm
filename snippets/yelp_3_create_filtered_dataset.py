# Review file
import sys

import pandas as pd

sys.path.append('../')

import snippets.yelp_constants_columns as cols
import snippets.yelp_constants_file_paths as paths
from snippets import get_logger


if __name__ == '__main__':
    """
    This code snippet creates a filtered Yelp Dataset based on the below criteria:
    - Only english reviews are considered
    - Only review whose length are above a certain threshold determined statistically are considered
    """

    # get the logger
    LOGGER = get_logger("snippet_create_filtered_dataset.out")

    # read the pickle
    LOGGER.debug("Reading the pickle....")
    reviews = pd.read_pickle(paths.PKL_FILE_REVIEW_ALL_LANG)

    # print the total number of reviews
    LOGGER.info("Total number of reviews: " + str(len(reviews)))

    # ------------------------ Deleting reviews less than 15 words --------------
    threshold = 15

    LOGGER.debug("Deleting the reviews whose length is less than 15 words")
    reviews.drop(reviews[reviews[cols.REVIEW_LENGTH] < threshold].index, inplace=True)

    # ------------------------ Deleting reviews not in english -------------------
    LOGGER.info("No of reviews not in english: " + str(len(reviews[reviews[cols.LANGUAGE] != 'en'])))

    LOGGER.debug("Deleting reviews not in english")
    reviews.drop(reviews[reviews[cols.LANGUAGE] != 'en'].index, inplace=True)

    # ------------------------ Final review count -------------------------------
    LOGGER.info("Total number of reviews: " + str(len(reviews)))

    # ------------------------ Storing the results -------------------------------

    # sort by the data
    LOGGER.debug("Sorting the reviews by date.....")
    reviews.sort_values(cols.DATE, inplace=True)

    # drop the user_id, language, review_length, boxcox
    LOGGER.debug("Dropping irrelevant columns.....")
    reviews.drop([cols.USER_ID, cols.LANGUAGE, cols.REVIEW_LENGTH], axis=1, inplace=True)

    # set the date and review_id as the index
    LOGGER.debug("Setting the index.....")
    reviews.set_index([cols.DATE, cols.REVIEW_ID], inplace=True)

    # write the results to a file for further processing (pkl format)
    LOGGER.debug("Writing the pickle file.....")
    reviews.to_pickle(paths.PKL_FILE_REVIEW_FILTERED)

