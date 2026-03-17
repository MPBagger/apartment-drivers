import pandas as pd
import numpy as np
import re

class CleanDate:
    """
    Class to clean and process data related to apartment listings.
    """

    def __init__(self):
        """
        Initializes the CleanDate object.
        """
        self.raw = pd.read_csv('data/raw.csv')
        self.current_year = 2026
        self.raw_columns = self.raw.columns
        self.clean_columns = self.snake_case()
        self.clean_data = self.clean_data()

    def snake_case(self):
        """
        Converts column names to snake case.

        Returns:
            pandas.Index: The column names in snake case.
        """
        return (self.raw_columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
                .str.replace(" ", "_")
                )

    def clean_data(self):
            """
            Cleans the raw data and returns the cleaned DataFrame.

            This method performs a series of data cleaning operations on the raw data, including:
            - Renaming columns to standardized names
            - Creating new columns based on existing columns
            - Filtering out non-apartment listings
            - Dropping unnecessary columns
            - Handling missing values

            Returns:
                pandas.DataFrame: The cleaned DataFrame.

            """
            df = self.raw.copy()
            df.columns = self.clean_columns
            df = df.assign(
                price = lambda x: pd.to_numeric(x.price, errors='coerce'),
                age = lambda x: self.current_year - x.build_year,
                time_on_market = lambda x: x.days_for_sale,
                price_weighted_sqm = lambda x: x.squaremeter_price,
                size_sqm = lambda x: x['size'],
            )

            df.reset_index(drop=True, inplace=True)
            df = df.replace(np.nan, None)

            df = df.drop(columns = ['address', 'build_year', 'days_for_sale'
                                    , 'squaremeter_price', 'size'
                                    , 'street', 'latitude', 'longitude'
                                    ])
            
            df.dropna(inplace=True)
            return df

    def __call__(self):
        """
        Returns the cleaned DataFrame.

        Returns:
            pandas.DataFrame: The cleaned DataFrame.
        """
        return self.clean_data()

if __name__ == '__main__':
    DF = CleanDate()
    DF.clean_data.tail(40)
    DF.clean_data.info()
    DF.raw.info()

