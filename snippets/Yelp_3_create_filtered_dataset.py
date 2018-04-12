# Review file
import sys
import pandas as pd
import numpy as np
from scipy.stats import boxcox
from scipy.special import inv_boxcox

sys.path.append('../')

import snippets.constants_yelp_dataset_columns as cols
import snippets.constants_yelp_dataset_file_paths as paths
from snippets import get_logger


BOXCOX = 'boxcox'

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

    # ------------------------ Deleting blank reviews ----------------------
    count = len(reviews[pd.isnull(reviews[cols.TEXT])])
    LOGGER.info("No of reviews with no text: " + str(count))

    LOGGER.debug("Deleting review with no text")
    reviews.drop(reviews[pd.isnull(reviews['text'])].index, inplace=True)

    # ------------------------ Calculating the box-cox transformation --------
    LOGGER.info("Review length statistics")
    LOGGER.info(reviews[cols.REVIEW_LENGTH].describe())

    LOGGER.debug("Calculating the box-cox transformation of the review lengths")
    reviews[BOXCOX] = boxcox(reviews[cols.REVIEW_LENGTH])[0]

    LOGGER.info("Box-cox transformed review length statistics")
    LOGGER.info(reviews[BOXCOX].describe())

    LOGGER.info("A review is short if its boxcox transformed value is less than (mean - 2 * stdDev)")
    mean = reviews[BOXCOX].mean()
    stdDev = reviews[BOXCOX].std()
    threshold = mean - (2 * stdDev)

    LOGGER.info("Calculated box-cox threshold: " + str(threshold))
    LOGGER.info("Calculated review length threshold: " + str(inv_boxcox(np.array(threshold), 0)))
    LOGGER.info("No of reviews whose length is less than the threshold: " + str(len(reviews[reviews[BOXCOX] < threshold])))

    LOGGER.debug("Deleting the reviews whose length is less than the threshold")
    reviews.drop(reviews[reviews[BOXCOX] < threshold].index, inplace=True)

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
    reviews.drop([cols.USER_ID, cols.LANGUAGE, cols.REVIEW_LENGTH, BOXCOX], axis=1, inplace=True)

    # set the date and review_id as the index
    LOGGER.debug("Setting the index.....")
    reviews.set_index([cols.DATE, cols.REVIEW_ID], inplace=True)

    # write the results to a file for further processing (pkl format)
    LOGGER.debug("Writing the pickle file.....")
    reviews.to_pickle(paths.PKL_FILE_REVIEW_FILTERED)

