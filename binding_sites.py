import pandas as pd
import numpy as np
import re

def what_site(amino_acid):
    """There are 6 binding sites (1A, 1B, 2A, 2B, 3A, 3B). The range in which each of them belongs to specific on
    can be found in bind_domains.csv. This function returns amino acid's binding site 
    give an integer between 1 and 582"""
    bind_sites = pd.read_csv(r"C:\Users\piotr\.ipython\Molecular Dynamics\Files\bind_domains.csv")
    for index, row in bind_sites.iterrows():
        # Check if the number falls between res_min and res_max
        if row['res_min'] <= amino_acid <= row['res_max']:
            return row['site_name']

def assign_binding_site(file):
    """This function creates table describing binding site. Namely, it shows
    what binding sites are in contact with hyaluronan molecule and what amino acids composition
    'Contacting receptor residues' are present"""
    data = pd.read_csv(file)
    pattern_aa = '[A-Z]+[A-Z]+[A-Z]'
    pattern_no = '\d+'
    amino_acids = []
    numbers = []
    for index, row in data.iterrows():
        # Look for 3 letter abreviations of amino acids
        amino_acids.append(re.findall(pattern_aa, row['Contacting receptor residues']))
        # Find positions in primary structure
        num = re.findall(pattern_no, row['Contacting receptor residues'])
        num = [what_site(int(item)) for item in num]
        numbers.append(num)
    merged_list_aa = sum([sublist for sublist in amino_acids], [])
    unique_val = np.unique(merged_list_aa)
        
    return unique_val

def main():
    file = r"C:\Users\piotr\.ipython\Molecular Dynamics\Files\Binding_sites.csv"
    d = assign_binding_site(file)
    print(d)
    print(what_site(510))
if __name__=="__main__":
    main()