# Review file
import multiprocessing
from datetime import datetime

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from textacy.text_utils import detect_language

import sys

sys.path.append('../')

import snippets.yelp_constants_columns as cols
import snippets.yelp_constants_file_paths as paths
from snippets import get_logger


def detect_lang(text):
    """
    Detects the language of the specified text
    :param text: the text for which the language is to be detected
    :return: a two letter character identifying the language of the text
    """
    try:
        return detect_language(text)
    except:
        return


def run_in_parallel(df_grouped, func):
    """
    Run the function in parallel on different groups
    :param df_grouped: grouped dataframe
    :param func: the function to run
    :return: the result of parallel processing
    """
    ret_lst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in df_grouped)
    return pd.concat(ret_lst)


def process_data_frame(df):
    """
    Function to process the data frame. Finds the length of the text and the language
    :param df: the data frame to process
    :return: the processed data frame
    """
    # detect the language of the text
    df[cols.LANGUAGE] = df[cols.TEXT].apply(detect_lang)

    # find the length of the review
    df[cols.REVIEW_LENGTH] = df[cols.TEXT].apply(lambda x: 0 if pd.isnull(x) else len(x.split()))
    return df


if __name__ == '__main__':
    """
    This code snippet detects the language and length of the reviews and 
    writes the results to a file 
    """

    # get the logger
    LOGGER = get_logger("snippet_detect_language.out")

    # read the data in batches
    batches = pd.read_csv(filepath_or_buffer=paths.CSV_FILE_REVIEW,
                          chunksize=1000,  # batch size
                          iterator=True,
                          usecols=[cols.REVIEW_ID, cols.BUSINESS_ID, cols.USER_ID, cols.DATE, cols.STARS, cols.TEXT],  # columns to read
                          parse_dates=[cols.DATE])

    # create an empty dataframe to store the results
    reviews = pd.DataFrame()

    # Read the review file
    LOGGER.info("Reading csv file......")
    for batch in batches:
        dfGroup = batch.groupby(np.arange(len(batch)) // multiprocessing.cpu_count())
        batch = run_in_parallel(dfGroup, process_data_frame)

        # append batches
        reviews = reviews.append(batch, ignore_index=True)

        # print progress after every 1000 reviews that have been processed
        if reviews[cols.REVIEW_ID].count() % 1000 == 0:
            LOGGER.debug(str(reviews[cols.REVIEW_ID].count()) + " : " + str(datetime.now()))

    # write the results to a file for further processing (pkl format)
    LOGGER.info("Writing pickle......")
    reviews.to_pickle(paths.PKL_FILE_REVIEW_ALL_LANG)

    # write the results to a file for further processing (csv format)
    LOGGER.info("Writing csv......")
    reviews.to_csv(paths.CSV_FILE_REVIEW_ALL_LANG, index=False, line_terminator='%\n', chunksize=1000, escapechar="\\")
