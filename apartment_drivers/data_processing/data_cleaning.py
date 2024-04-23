import pandas as pd
import numpy as np
import re

class CleanDate:
    def __init__(self):
        self.raw = pd.read_csv('data/raw.csv')
        self.current_year = 2024
        self.raw_columns = self.raw.columns
        self.clean_columns = self.snake_case()
        self.clean_data = self.clean_data()

        
    def snake_case(self):
        return (self.raw_columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
                .str.replace(" ", "_")
                )
    
    def clean_data(self):
        df = self.raw.copy()
        df.columns = self.clean_columns
        df = df.assign(
            appartment = lambda x: x.til_salg.str.contains('lejlighed'),
            price = lambda x: x.price.str.replace('.', '').str.replace(' kr', '').astype(float),
            renovated_in_last_10_years = lambda x: self.current_year-10 <= x.renov,
            age = lambda x: self.current_year - x.built,
            time_on_market = lambda x: x.time_on_market_b,
            price_weighted_sqm = lambda x: x.sqm_pr,
            size_sqm = lambda x: x.til_salg.str.extract('(\d+) m²'),

            )

        df = df[df.appartment == True]
        df.reset_index(drop=True, inplace=True)
        df = df.replace(np.nan, None)

        df = df.drop(columns = ['address', 'til_salg', 'period', 'from'
                                , 'appartment', 'pay', 'fees', 'renov'
                                , 'time_on_market_a', 'time_on_market_b'
                                , 'floor_lvl', 'o_wall', 'sqm_pr', 'area'
                                , 'roof', 'value', 'last_price', 'til_leje'
                                , 'depo', 'size', 'sqm', 'garage'
                                ])
        
        df.dropna(inplace=True)
        return df

    def __call__(self):
        return self.clean_data()

if __name__ == '__main__':
    DF = CleanDate()
    DF.clean_data.tail(40)
    DF.clean_data.info()


