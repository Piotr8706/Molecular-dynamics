import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from typing import Tuple


def what_site(amino_acid: int) -> str:
    """
    There are 6 binding sites (1A, 1B, 2A, 2B, 3A, 3B). The range in which each of them belongs to specific on
    can be found in bind_domains.csv. This function returns amino acid's binding site 
    give an integer between 1 and 582
    """
    bind_sites = pd.read_csv(r"C:\Users\piotr\.ipython\Molecular Dynamics\Files\bind_domains.csv")
    for _, row in bind_sites.iterrows():
        # Check if the number falls between res_min and res_max
        if row['res_min'] <= amino_acid <= row['res_max']:
            return row['site_name']
        
def assign_binding_site(file: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    This function creates table describing binding site. Namely, it shows
    what binding sites are in contact with hyaluronan molecule and what amino acids composition
    'Contacting receptor residues' are present
    """
    data = pd.read_csv(file)
    pattern_aa = '[A-Z]{3}'
    pattern_no = '\d+'
    # finding 3 letter abreviations of amino acids
    amino_acids = data['Contacting receptor residues'].str.findall(pattern_aa)
    # finding positions to assign them into HSA domains
    numbers = data['Contacting receptor residues'].str.findall(pattern_no).apply(lambda x: [what_site(int(item)) for item in x])

    # calculating number of occurences of both amino acid composition and how many contacts with each domain
    # a particular docked position has
    merged_list_aa = np.concatenate(amino_acids)
    merged_list_num = np.concatenate(numbers)
    unique_val_aa = np.unique(merged_list_aa, return_counts=False)
    unique_val_site = np.unique(merged_list_num, return_counts=False)
    count_amin_acid = []
    count_site_domain = []
    lines = data.shape[0]

    for k in range(0,lines):
        for j in range(0,len(unique_val_aa)):
            count_amin_acid.append(len([i for i in amino_acids[k][:] if i==unique_val_aa[j]]))
        for j in range(0,len(unique_val_site)):
            count_site_domain.append(len([i for i in numbers[k][:] if i==unique_val_site[j]]))
            
    count_amin_acid = np.array(count_amin_acid).reshape(lines,-1)
    count_site_domain = np.array(count_site_domain).reshape(lines,-1)

    # joining arrays to display in plt.table
    combined_table = np.concatenate((count_amin_acid, count_site_domain), axis=1)
    labels = np.concatenate((unique_val_aa,unique_val_site))
    return combined_table, labels

def create_table(file_path: str) -> None:
    """
    Genarates and prints a table showing info about binding site
    """
    data, labels_joined = assign_binding_site(file_path)
    docked_positions = list(range(1, data.shape[0]+1))

    fig, ax = plt.subplots()
    ax.axis('off')
    data_to_str = np.array(data, dtype=str)
    table = ax.table(cellText=data_to_str, rowLabels=docked_positions, colLabels=labels_joined, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1.2, 1.5)
    #plt.savefig('./Files/Bind_table.png')
    df = pd.DataFrame(data)
    headers = labels_joined
    df.index = df.index + 1
    df.to_csv('./Files/Biding_sites_summary.csv', header=headers, index_label='Dock_site')
    plt.show()

def main():
    file = r"C:\Users\piotr\.ipython\Molecular Dynamics\Files\Binding_sites.csv"
    create_table(file)

if __name__=="__main__":
    main()