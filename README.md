# 2021 SIGMOD Programming Contest

### DBGroup@SUSTech

## Contest Overview

**Task:** 

Given records extracted from various website, we aim to solve the entity resolution problem, namely whether two records points to the same real world object.

**Input:** 

Three datasets (records are only compared with other records in the same dataset)

**Output:**

 All pair of records pointing to the same real world objects

**Measurement:** 

F-score

## Getting Started

1. Install python 3 if you haven't get one.
2. Download and unzip this project.
3. Execute `run.py` by `python run.py` and please make sure that the csv files `X2.csv`, `X3.csv` and `X4.csv` for original datasets are inside the project folder.
4. All matched pairs will be placed in `output.csv`.

## System Architecture

The architecture of our work can be divided into two parts, data cleaning and entity matching.

#### Data Cleaning

In this part, we reorganize and clean the given csv files row by row. Cleaned results with only key field values for each row are returned. Codes for  `X2.csv`, `X3.csv` and `X4.csv` are provided in `clean_x2.py`, `clean_x3.py`, and `clean_x4.py` respectively. The detailed steps are described as follows.

**Preprocessing:** Columns in the same row are merged together and changed into lowercase.

**Attributes Extraction:** Key information such as brand are extracted from each row through their corresponding regular rules. The regular rules are designed based on the given datasets and other descriptions from e-commerce websites or the official website of the brand. Note that`'0'` represents a missing value in this key field.

**Attributes Correction:** Different expressions of a key field with the same meaning are translated to the same expression. What's more, we tried our best to fill the missing values according to other existing field values of the same row.

**Return:** Finally, key field values are organized into a dataframe and returned.

#### Entity Matching

In this part, we give each record an identification according to its key field values and do entity resolution for records according to their identification values. Codes for  `X2.csv`, `X3.csv` and `X4.csv` are provided in `handler_x2.py`, `handler_x3.py`, and `handler_x4.py` respectively. Note that `clean_x2.py` is called by `handler_x2.py` and so forth. The detailed steps are given as follows.

Original csv file is turned into cleaned dataframe and significant fields are picked out. If there is no missing value among these fields of a record, they are used as the unique identification for this record and we add this record to list `solved_spec`.  Otherwise, we do not give the record an identification and add it to list `unsolved_spec`. Note that we can classify all the records into several groups and use different fields as the identification for records in different groups.

For records in `unsolved_spec`, we try to match them to items in `solved_spec`.  Since at least one important filed value is missing for records in `unsolved_spec`, we use their secondary key values. We give several combinations of secondary key values based on observation of real data. The identification of items in `solved_spec` is assigned to identification of items in `unsolved_spec` while we move items in `unsolved_spec` to `solved_spec` if they obtain the same nonzero secondary key values under one combination.

For records still in `unsolved_spec`,  we also give them a general identification value which as not as tight  and correct as the previous ones. This helps us make a rough classification for items still without identification values after step 1 and 2.

**Return:** Lastly, we regard items with the same identification values as the same entities in real world and match them. The matched items are saved as our output in `output.csv`.

## Result
| ---- | ---- | ---- | ---- |
| Dataset | Recall | Precision | F-score |
| X2.csv |  |  |  |
| X3.csv |  |  |  |
| X4.csv |  |  |  |
