import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
"""Początek"""

def main():
    file = r"C:\Users\piotr\Downloads\Results\Results\Mg_contacts_11.txt"
    df = pd.read_csv(file, delimiter='\t')  # Assuming it's a tab-delimited file. Adjust delimiter as needed.

    # Display the first few rows of the dataframe
    print(df.head())
    print(df.info())
    print(df.describe())


if __name__=='__main__':
    main()