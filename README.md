# Reproduction of the Paper "Mining the Peanut Gallery: Opinion Extraction and Semantic Classification of Product Reviews" as part of my NLP course at MLU Halle-Wittenberg (2019)

## Requirements
- Python 3.7
- Jupyter 1.0.0_5
- Pandas 0.24.2
- tqdm 4.31.1
- NLTK 3.4
- scikit-learn (sklearn) 0.21.2


## Installation & run Jupyter Notebook

- Install Jupyter Notebook (e.g. `brew install jupyter`)
- `git clone https://github.com/Valentindi/reproduction-mining-the-peanut-gallary.git`
- `cd reproduction-mining-the-peanut-gallary`
- `pip install -r src/Requirements.txt`
- `jupyter-notebook`

## Get Data
- Download 7 subsets of the [Amazon Customer Reviews Dataset](https://s3.amazonaws.com/amazon-reviews-pds/readme.html). I selected the following categories: 'mobile_electronics', 'watches', 'home entertainment', 'tools', 'electronics', 'sports', 'wireless'. It should work with other categories as well.
- Merge the downloaded files (Maybe it's a good idea to concat a small split of the large files) and call move the file to `data/amazon.csv`. (you can edit filenames and paths in the python scripts.)
- run `python src/preprocess.py`. This scripts removes not valid datasets, concats review title and body, tokenize reviews and calculates a boolean rating based on the amazon 5-star-rating.
- run `python src/create_dataset.py`. This scripts creates a dataset with similar size as the authors of the original paper.
- run `python src/replace_rare_words_and_numbers.py`. This Scripts replaces numbers with a unique Token and replaces words, which occures less or equal 10 times within the dataset. (You can change the threshold in the file.)


## Run Experiments
- open your Jupyter Notebook in the browser, open the subdirectory `src`and run the Notebook `create_train_test_splits.ipynb`. This Notebook creates train/test splits for test 1 and test 2.
- now you can run the Experiments `Table1_2.ipynb`, `Table3-4-6.ipynb` and `Table8.ipynb`.

