import pandas as pd
from nlpwebapp.scraper.py import RottenTomatoesScraper

print(pd.DataFrame(RottenTomatoesScraper("https://www.rottentomatoes.com/m/parasite_2019").to_dict()))