import sys

import gc
import numpy as np
import pandas as pd
import plac
from joblib import Parallel, delayed
from textacy import Corpus
import os

sys.path.append('../')
from src.transformers import preprocessor as pr
import snippets.constants_yelp_dataset_columns as cols
import snippets.constants_yelp_dataset_file_paths as paths
from datetime import datetime


@plac.annotations(
    n_jobs=("Number of workers", "option", "n", int),
    batch_size=("Batch-size for each process", "option", "b", int)
)
def main(n_jobs=3, batch_size=12):
    """
    This code snippet applies a pre-processing technique to a review and then subsequently stores the
    ngrams for the pre-processed text
    """
    summary_files = {
        "weekly": paths.DIR_FILE_REVIEW_WEEKLY,
        "monthly": paths.DIR_FILE_REVIEW_MONTHLY
    }

    for type, folder in summary_files.items():
        preprocess(folder, n_jobs, batch_size)


def preprocess(folder, n_jobs=3, batch_size=12):
    # -------------------------- Initialization ----------------------------
    # read the summary file
    summary = pd.read_pickle(os.path.join(folder, "summary" + paths.EXT_PKL))

    # ----------------------- Read the files --------------------------
    print("{0} - Reading files......".format(str(datetime.now())))

    dfs = np.array_split(summary, batch_size)
    Parallel(n_jobs=n_jobs)(delayed(transform_texts)("en", folder, batch)
                            for i, batch in enumerate(dfs))


def transform_texts(lang, folder, batch):
    for index, row in batch.iterrows():
        batch_id = row['filename']

        if os.path.isfile(os.path.join(folder, paths.DIR_PRE_PROCESSED, batch_id)):
            continue

        # ------------------ Loading Data -----------------
        print("{0} - Loading data: {1}".format(str(datetime.now()), str(batch_id)))

        data = pd.read_pickle(os.path.join(folder, paths.DIR_RAW, batch_id))

        print("{0} - Data loaded: {1}".format(str(datetime.now()), str(batch_id)))

        # ------------------ Start Preprocessing -----------------
        print("{0} - Pre-Processing data: {1}".format(str(datetime.now()), str(batch_id)))

        # set the parameter
        replace_urls = True
        replace_emoticons = True
        replace_exclamations = False
        replace_punctuations = False
        replace_numbers = False
        replace_negations = True
        replace_colloquials = False
        replace_repeated_letters = True
        replace_contractions = True
        replace_whitespace = True
        replace_currency = True

        data[cols.TEXT] = data[cols.TEXT].apply(lambda x: pr.run_preprocessor(x, replace_urls=replace_urls,
                                                                              replace_emoticons=replace_emoticons,
                                                                              replace_exclamations=replace_exclamations,
                                                                              replace_punctuations=replace_punctuations,
                                                                              replace_numbers=replace_numbers,
                                                                              replace_negations=replace_negations,
                                                                              replace_colloquials=replace_colloquials,
                                                                              replace_repeated_letters=replace_repeated_letters,
                                                                              replace_contractions=replace_contractions,
                                                                              replace_whitespace=replace_whitespace,
                                                                              replace_currency=replace_currency,
                                                                              replace_currency_with=" CURRENCY ")
                                                )

        print("{0} - Pre-Processing completed: {1}".format(str(datetime.now()), str(batch_id)))

        # -------------------- End Preprocessing -----------------

        # -------------------- Start Corpus Creation -----------------

        print("{0} - Creating corpus: {1}".format(str(datetime.now()), str(batch_id)))

        data.reset_index(inplace=True, drop=False)

        corpus = Corpus(lang=lang,
                        texts=list(data[cols.TEXT]),
                        metadatas=data[[cols.DATE, cols.REVIEW_ID, cols.BUSINESS_ID, cols.STARS]].to_dict(
                            orient='records'))

        print("{0} - Corpus created: {1}".format(str(datetime.now()), str(batch_id)))

        # -------------------- End Corpus Creation -----------------

        print("{0} - Extracting ngrams: {1}".format(str(datetime.now()), str(batch_id)))
        text_stats = pd.DataFrame()
        for doc in corpus:
            # ------------------ Extract ngrams -----------------

            ngram = doc.to_bag_of_terms(ngrams=(1, 2, 3), named_entities=True, normalize='lemma', as_strings=True,
                                        filter_stops=True)

            metadata = doc.metadata.copy()
            del metadata[cols.REVIEW_ID]
            del metadata[cols.DATE]

            metadata["ngrams"] = np.asarray(ngram)

            # ------------------ Convert to Dataframe -------------------------
            # convert to a dataframe with the review_id as the index
            idx = pd.MultiIndex.from_arrays([[doc.metadata[cols.DATE]],
                                             [doc.metadata[cols.REVIEW_ID]]],
                                            names=[cols.DATE, cols.REVIEW_ID])
            text_stat = pd.DataFrame(metadata, index=idx)

            # append the rows
            text_stats = text_stats.append(text_stat)

        print("{0} - Processing complete: {1}".format(str(datetime.now()), str(batch_id)))

        # ------------------ Saving results -------------------------
        print("{0} - Saving pre-processed file: {1}".format(str(datetime.now()), str(batch_id)))

        text_stats.to_pickle(os.path.join(folder, paths.DIR_PRE_PROCESSED, batch_id))

        print("{0} - Saving completed file: {1}".format(str(datetime.now()), str(batch_id)))

        del data
        del corpus
        del text_stats

        gc.collect()


if __name__ == '__main__':
    plac.call(main)
