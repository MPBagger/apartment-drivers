# MLflow project - example

We will create a project where we will use mlflow for experiment tracking.
The project will be based on the example case (here the apartment price driver example case)

#### new project

Let's create a new poetry project

```shell
poetry new apartment-drivers
```

Adding needed packages

```shell
cd apartment-drivers
poetry add pandas scikit-learn requests beautifulsoup4 lxml 
```

```shell
poetry install
```

#### initialize the git project

```shell
git init
git add .
git commit -m "initial commit of the apratment-drives project"
```

## Data

We need to get the data for the project. We will have to scrape this data.
We will create a scrapet and a crawler to retrieve the data and save the data as a flat file (for experimentation). Preferably we would create a continous (or schedueled) data pipeline that would scrape the data on a continous basis (eg. daily)

In the folder `apartment_drivers` we will create a folder called `data_collection`.

```shell
cd apartment_drivers
mkdir data_collection
```

We will create the following scripts in the folder:

- `crawler.py` containing the definition of the crawler we want to use for crawling boligsiden.dk.
- `scraper.py` containing the scraper to be used on the urls from the crawler.
- `main.py` defining the pipeline for retrieving the data (using the crawler and the scraper)

when the three scripts are done they are pushed to git.

Afterwards we created a folder called `data_processing` (also in the `apartment_drivers` folder)

```shell
mkdir data_processing
```

in this folder we will create a data cleaning script called `data_cleaning.py`

## Machine Learning

Before we start running ML models we will install mlflow in our poetry env.

```shell
poetry add mlflow
```

You can read about mlflow [here](https://mlflow.org/docs/latest/introduction/index.html)
mlflow provides you with a local UI that allows you to perform e.g. experiment tracking. You can access the ui by running the following command:

```shell
poetry run mlflow ui
```

we will create a new folder for our ml scripts called `model_training` and a script called `model_training.py`. This script holds the logic for both running a logistic regression and logging to mlflow.

In the `apartment_drivers` folder we will create a `main.py` which will call classes and functions from the other scripts and be used to execute a simple pipeline.
