---
pandoc_args: ["--toc", "--toc-depth=2"]
geometry: "left=2cm,right=2cm,top=3cm,bottom=3cm"
export_on_save:
    pandoc: true
output:
    pdf_document:
        toc: true
        number_sections: true
links-as-notes: true
linkcolor: blue
documentclass: article
papersize: a4
hyperrefoptions:
- linktoc=all
link-citations: true
header-includes:
    - \usepackage{amsmath}
    - \usepackage{float}
    - \usepackage{graphicx}
    - \restylefloat{figure}
title: Network Operating System
subtitle: Developing market-worthy models using cloud developement
abstract: \
    In following document we share our route for developement of the project infrastructure.
author:
- Paweł Pozorski, Zuzanna Sieńko
date: "2024-12-23"
lang: en-EN
---

\newpage{}

# Deploying model using Snowpark, python and VS Code

## Creating trial Snowflake Account

For purpose of the project we'll use free, trial Snowflake account that is avaliable for public for up to 30 days / 400 USD of credits. As our cloud provider, we'll choose AWS as it was introduced on the labs.

\

\begin{center}
    \includegraphics[height=0.4\textheight]{assets/image.png}
    \\
    \text{Registration form.}
\end{center}

Using snowsight, we create basic setup for snowflake:
```snowsql
CREATE WAREHOUSE IF NOT EXISTS ml_warehouse
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60  -- Automatically suspends after 60 seconds of inactivity
  AUTO_RESUME = TRUE;

CREATE ROLE IF NOT EXISTS DATA_SCIENTIST;
GRANT ROLE DATA_SCIENTIST TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON WAREHOUSE ml_warehouse TO ROLE DATA_SCIENTIST;

CREATE DATABASE ml_database;
CREATE SCHEMA datasets;

GRANT OWNERSHIP ON DATABASE ml_database TO ROLE DATA_SCIENTIST;
GRANT OWNERSHIP ON SCHEMA datasets TO ROLE DATA_SCIENTIST;
```

Now let's try to access it from snowpark. For installation we've followed [these instructions](https://docs.snowflake.com/en/developer-guide/snowpark/python/setup). After providing required connection details described [here](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections), we create simple code to validate if it works correctly:
```python
from snowflake.snowpark import Session
from snowflake.ml.utils.connection_params import SnowflakeLoginOptions

options = SnowflakeLoginOptions(login_file=".snowsql/config", connection_name="ml")

sp_session = Session.builder.configs(options).create()

sp_session.sql("DESCRIBE DATABASE ml_database;").collect()
```

Recieving:
```bash
[Row(created_on=datetime.datetime(2024, 12, 24, 13, 6, 41, 881000, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>), name='DATASETS', kind='SCHEMA'),
 Row(created_on=datetime.datetime(2024, 12, 24, 13, 34, 5, 265000, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>), name='INFORMATION_SCHEMA', kind='SCHEMA')]
```

## Loading data

Here we've downloaded our dataset of choice ([source](https://archive.ics.uci.edu/static/public/9/auto+mpg.zip")), unzipped it and made some adjustments to its structure (those normally wouldn't be neccessary, but this dataset is very old and it does not follow normal csv encoding standards, therefore we've used slow regex convertion to fix them). Next steps were again cloud-related:

- create stage on snowflake - for those unfamilliar with that technology, stage is place on our cloud where we can put our files. In our case, it will use azure cloud file system to accomplish that.
- put the file into the stage
- scheck if it is present there 

    | name                                  | size  | md5                                | last_modified               |
    |---------------------------------------|-------|------------------------------------|-----------------------------|
    | auto_mpg_stage/auto-mpg.data         | 30288 | b26b22a6...   | Sat, 4 Jan 2025 15:01:04 GMT |

    Here we can also see that snowflake automatically stores some metadata on our file - its modification date, size and md5 hash. Thats usefull for production usage because whenever we overwrite such file and try to load it into table again, snowflake will check if it's hash has changed. If not, it will skip data loading to avoid repetitions (providing we won't force load it)

- create sql table to store data from our file - below is final table structure used for training (after some transformations described later we dropped some columns, also ID column gets finally dropped as well).

    ```bash
    root
    |-- "MPG": DoubleType() (nullable = True)
    |-- "CYLINDERS": LongType() (nullable = True)
    |-- "DISPLACEMENT": DoubleType() (nullable = True)
    |-- "HORSEPOWER": DoubleType() (nullable = True)
    |-- "WEIGHT": DoubleType() (nullable = True)
    |-- "ACCELERATION": DoubleType() (nullable = True)
    |-- "MODEL_YEAR": LongType() (nullable = True)
    |-- "ORIGIN": LongType() (nullable = True)
    ```

- create file format - or those unfamilliar with that technology, file format is abstract object that tells snowsql how to load data - here we can define its type, endoding, how to treat null values and many more. 
- load data into table 

    | file                                 | status | rows_parsed | rows_loaded | error_limit |
    |--------------------------------------|--------|-------------|-------------|-------------|
    | auto_mpg_stage/cleaned-auto-mpg.data | LOADED | 398         | 398         | 1           |

    | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
    |-------------|-------------|------------------|------------------------|-------------------------|
    | 0           | NULL        | NULL             | NULL                   | NULL                    |

    Here we can also debug our file format - if any error occurs, we will be able to address that. For production usage we can also set in our file format how many errors are acceptable and more. 

## EDA

Before we bagin, this part aims to show power of cloud resources not to be a compleate data science project. Therefore, below we show some basic calculations performed in snowpark. Each havy-calculation part is performed natively on cloud, so this code can be used on very large datasets as well.

...

## Model

We'll be using XGBRegressor as it is a model that can fit any data distribution well and our data is not that large. Morover, this model allows for advanced parameter tuning. To showcase Snowflake power we'll be using model registry to deploy models. 

...

## Accessing model
