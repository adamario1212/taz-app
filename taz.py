import pandas as pd
import numpy as np

# building the data
file = ("C:\\code\\taz.csv")
taz_file = pd.read_csv(file)
taz_file["תחמושת"] = taz_file["תחמושת"].astype(str).str.replace(r",", "", regex=True)
taz_file["תחמושת"] = taz_file["תחמושת"].astype(float)


def how_much(amount, row):
    ammo_value = taz_file.iloc[row]["תחמושת"] 
    total = ammo_value * amount
    return total, taz_file.iloc[row]["שם"]

rimon = how_much(100, 0)
print(rimon)
    


