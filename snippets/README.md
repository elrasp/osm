# Running the Snippets

The information belows describes the steps to build the Amazon and Yelp data streams, preprocess the data and learn over the stream using an active learner that is irregularly available.

## Construcing the Data Streams

### Amazon Dataset specific instructions
- Download the 5-core datasets for

-- Beauty

-- Cell Phones and Accessories

-- Clothing, Shoes and Jewelry

-- Electronics

-- Home and Kitchen

-- Apps for Android

-- CDs and Vinyls

-- Health and Personal Care

-- Kindle Store

The downloaded files need to be placed in ../data/amazon

- Convert the dataset to pickle with only the required data.

-- Snippet: amazon_1_convert_to_pickle.py

-- Output: ../data/amazon/*.json.gz -> ../data/amazon/*.pkl.gzip

- Construct the dataset from 2011 onwards varying the product categories every 3 months

-- Snippet: amazon_2_construct_dataset.py

-- Output: ../data/amazon/*.pkl.gzip -> ../data/amazon/filtered/review.pkl.gzip


### Yelp Dataset specific instructions
- Download the .json files for the Yelp dataset and put them in ../data/yelp/json

- Convert to csv

-- Snippet: yelp_1_convert_json_to_csv_python2.py. Note: run this script in Python 2

-- Output: ../data/yelp/json/review.json -> ../data/yelp/csv/review.csv

- Determine the language and review length (very long running)

-- Snippet: yelp_2_detect_language.py

-- Output: ../data/yelp/csv/review.csv -> ../data/yelp/lang/review.pkl.gzip

- filter the dataset for english reviews and remove those reviews that have  less than 15 words

-- Snippet: yelp_3_create_filtered_dataset.py

-- Output: ../data/yelp/lang/review.pkl.gzip -> ../data/yelp/filtered/review.pkl.gzip

### Common instructions

- Create weekly batches of the data

-- Snippet: \*_create_time_series_file_splits.py

-- Output:  \*/filtered/review.pkl.gzip -> data split weekly \*/filtered/weekly/raw/\*.pkl.gzip and the summary of the stream \*/filtered/weekly/summary.pkl.gzip

- Preprocess the data (very long running)

-- Snippet: \*_preprocess_reviews.py

-- Output:  \*/filtered/weekly/raw/\*.pkl.gzip -> \*/filtered/weekly/preprocessed/\*.pkl.gzip

- Convert to 3 class problem

-- Snippet: \*_convert_stars.py

-- Output: \*/weekly/preprocessed/\*.pkl.gzip -> \*/weekly/converted/\*.pkl.gzip and \*/weekly/summary.pkl.gzip -> \*/weekly/summary_converted.pkl.gzip

- Run active learner with oracle available irregularly (long running)

-- Snippet: \*_main.py
use -a to specify the availability. Can be in the range (0, 1]

-- Ouput: \*/filtered/results
