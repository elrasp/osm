import sys

import pandas as pd
import plac
import os
from datetime import datetime

sys.path.append('../')
import snippets.constants_amazon_dataset_file_paths as paths
import snippets.constants_amazon_dataset_columns as cols


def main():
    """
    This code snippet generate the initially labeled data
    """

    # set the input folder
    input_folder = paths.DIR_FILE_REVIEW_WEEKLY
    unprocessed_folder = os.path.join(input_folder, paths.DIR_PRE_PROCESSED)
    summary_filename = "summary" + paths.EXT_PKL

    # read the summary file
    summary = pd.read_pickle(os.path.join(input_folder, summary_filename))
    summary = summary.sort_index()

    path = os.path.join(input_folder, "converted")
    if not os.path.exists(path):
        os.mkdir(path)

    for index, row in summary.iterrows():

        # read the data
        print(row['filename'])
        data = pd.read_pickle(os.path.join(unprocessed_folder, row['filename']))

        # convert stars
        # 1, 2 -> negative
        # 3 -> neutral
        # 4, 5 -> positive
        if not data.empty:
            if not data.loc[data[cols.STARS] == 1].empty:
                data.loc[data[cols.STARS] == 1, cols.STARS] = 'negative'
            if not data.loc[data[cols.STARS] == 2].empty:
                data.loc[data[cols.STARS] == 2, cols.STARS] = 'negative'
            if not data.loc[data[cols.STARS] == 3].empty:
                data.loc[data[cols.STARS] == 3, cols.STARS] = 'neutral'
            if not data.loc[data[cols.STARS] == 4].empty:
                data.loc[data[cols.STARS] == 4, cols.STARS] = 'positive'
            if not data.loc[data[cols.STARS] == 5].empty:
                data.loc[data[cols.STARS] == 5, cols.STARS] = 'positive'

        # write the data
        data.to_pickle(os.path.join(input_folder, "converted", row['filename']))

        row['filename'] = os.path.join("converted", row['filename'])

    summary_filename = "summary_converted" + paths.EXT_PKL
    summary.to_pickle(os.path.join(input_folder, summary_filename))


if __name__ == '__main__':
    plac.call(main)
