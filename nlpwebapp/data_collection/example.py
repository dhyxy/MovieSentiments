import pandas as pd

from RottenTomatoesScraper import RottenTomatoesScraper

print(
    pd.DataFrame(
        RottenTomatoesScraper(
            "https://www.rottentomatoes.com/m/the_vault_2017/reviews?type=user"
        ).to_dict()
    )
)
