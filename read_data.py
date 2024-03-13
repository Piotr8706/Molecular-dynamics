import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def read_and_transform(file):
    """This project deals with three different type of file structure. The purpose of 
    this function is to read files with H-bonds and ionic interations which have following structure:
    40000000.000
    1.000 852.000 14.775 0 4.000 2.180
    8.000 55.000 25.000 1 56.000 1.996
    40100000.000
    8.000 55.000 25.000 1 56.000 2.100
    12.000 45.000 9.975 1 46.000 2.359
    12.000 898.000 20.725 0 13.000 1.981
    40200000.000
    8.000 55.000 23.450 1 56.000 1.997
    12.000 45.000 20.400 1 46.000 2.182
    etc
    should be converted into:
    40000000.000 1.000 852.000 14.775 0 4.000 2.180
    40000000.000 8.000 55.000 25.000 1 56.000 1.996
    40100000.000 8.000 55.000 25.000 1 56.000 2.100
    40100000.000 12.000 45.000 9.975 1 46.000 2.359
    40100000.000 12.000 898.000 20.725 0 13.000 1.981
    40200000.000 8.000 55.000 23.450 1 56.000 1.997
    40200000.000 12.000 45.000 20.400 1 46.000 2.182
    It starts with timestamp followed by list of all interactions of given type.
    Function puts time stamp in first column
    """
    with open(file, "r") as file:
        lines = file.readlines()

    # Initialize empty lists to store modified data
    modified_data = []

    for line in lines:
        # Split the line by whitespaces
        values = line.strip().split()

        # If the line contains a single value
        if len(values) == 1:

            timestamp = float(values[0])
        else:
            # Add the single value to the beginning of the row
            # TODO: make convert to float for column used pandas manipulation functions
            modified_row = [timestamp] + list(map(float, values[:]))
            modified_data.append(modified_row)

    # Convert the modified data into a DataFrame
    df = pd.DataFrame(modified_data)
    df.columns = ['Timestamp'] + [f'Col_{i}' for i in range(1, len(df.columns))]
    return df


def read_file_show_interaction(typ, parameter):
    """Reading all data from all files for a given ion that is added to the system"""
    Ca = []
    Na = []
    Mg = []
    path = r"C:\Users\piotr\Downloads\IJMS_HA+Albumin"
    match typ:
        case 'Bind':
            path = path + r"\Binding_energy"
        case 'Structural':
            path = path + r"\Structural"
        case 'HBond':
            path = path + r"\HBond"
        case 'Ionic':
            path = path + r"\Ionic"

    for i in range(1, 13):
        f1 = path + r"\Ca_" + str(i) + r".txt"
        f2 = path + r"\Mg_" + str(i) + r".txt"
        f3 = path + r"\Na_" + str(i) + r".txt"
        if typ == 'Bind' or typ == 'Structural':
            # Read the data, considering the structure provided
            data1 = pd.read_table(f1, delim_whitespace=True)
            data2 = pd.read_table(f2, delim_whitespace=True)
            data3 = pd.read_table(f3, delim_whitespace=True)
            Ca.append(data1[parameter][400:].mean())
            Mg.append(data2[parameter][400:].mean())
            Na.append(data3[parameter][400:].mean())
        else:
            f1_data = read_and_transform(f1)
            data1 = count_rows_with_conditions(f1_data )['Count'] 
            f2_data = read_and_transform(f2)
            data2 = count_rows_with_conditions(f2_data )['Count'] 
            f3_data = read_and_transform(f3)
            data3 = count_rows_with_conditions(f3_data )['Count'] 
            # TODO: data1.mean()
            Ca.append(data1.mean())
            Mg.append(data2.mean())
            Na.append(data3.mean())
    return np.array(Ca), np.array(Mg), np.array(Na)


def count_rows_with_conditions(df):
    """Counts number of interactions in time stamp. However we are only interested in 
    intermolecular interactions so that certain conditions must be applied. HSA atoms are in range
    1-9132, HA: 9133-10239, numbers above represent solvent atoms. Mind atom number is different from
    residue number. HSA is composed of 582 residues."""
    
    filtered_df = df[(df.iloc[:, 1] < 9133) & (df.iloc[:, 2] >= 9133) & (df.iloc[:, 1] < 10240) & (df.iloc[:, 2] < 10240)]
    if filtered_df.empty:
        return pd.DataFrame()
    
    count_df = filtered_df.groupby('Timestamp').size().reset_index(name='Count')
    
    return count_df
def create_figure_and_save(*args):
    
    fig = plt.figure()
    X = np.arange(0, len(args[0]))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    colors = ['b','g','r']
    labels = ['Ca','Mg','Na']
    for i in range(len(args)-3):
        ax.bar(X + 0.25*i, args[i], color=colors[i], width=0.25, label=labels[i])
    ax.set_title(args[3])
    ax.set_xlabel("Site")  # Added x-axis label
    ax.set_ylabel(args[4])
    plt.legend(loc='upper right')
    path = r"./Files/" + args[5] + r"_vs_site.png"
    plt.savefig(path)
    #plt.show()

def bind_sites():
    bind_sites = pd.read_csv('./Files/Biding_sites_summary.csv')
    # dividing amino acids into groups
    new_data = pd.DataFrame(columns=["Dock_site", "Charged+", "Charged-", "Hydrophobic", "Special", "1A+1B",  "2A+2B", "3A+3B",])

    # Copy columns from original data
    new_data["Dock_site"] = bind_sites["Dock_site"]
    new_data["Charged+"] = bind_sites["ARG"] + bind_sites["HIS"] + bind_sites["LYS"]
    new_data["Charged-"] = bind_sites["ASP"] + bind_sites["GLU"]
    new_data["Hydrophobic"] = bind_sites["ALA"] + bind_sites["VAL"] + bind_sites["ILE"] + bind_sites["LEU"]
    + bind_sites["MET"] + bind_sites["PHE"] + bind_sites["TYR"]
    new_data["Special"] = bind_sites["CYS"] + bind_sites["GLY"] + bind_sites["PRO"]
    new_data["1A+1B"] = bind_sites["1A"] + bind_sites["1B"]
    new_data["2A+2B"] = bind_sites["2A"] + bind_sites["2B"]
    new_data["3A+3B"] = bind_sites["3A"] + bind_sites["3B"]
    return new_data

def create_corr_matrix(data):
    corr = data.corr()
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontsize='x-small'  # Adjust font size as needed
    );
    plt.tight_layout()  # Adjust layout to prevent label overlapping
    plt.savefig('./Files/Correlation_matrix.png')

def main():
    
    # calculating interactions
    Ca_Ionic, Mg_Ionic, Na_Ionic = read_file_show_interaction('Ionic', '')
    Ca_HBond, Mg_HBond, Na_HBond = read_file_show_interaction('HBond', '')
    Ca_Bind, Mg_Bind, Na_Bind = read_file_show_interaction('Bind', 'Energy')
    Ca_Rg_HA, Mg_Rg_HA, Na_Rg_HA = read_file_show_interaction('Structural', 'Rg_HA')

    #Creating plots
    create_figure_and_save(Ca_Rg_HA, Mg_Rg_HA, Na_Rg_HA, "HA's Radius of gyration", "R_g [A]", "Rg")
    create_figure_and_save(Ca_HBond, Mg_HBond, Na_HBond, "Hydrogen Bonds", "# of H-bonds", "HBond")
    create_figure_and_save(Ca_Ionic, Mg_Ionic, Na_Ionic, "Ionic interactions", "# of interactions", "Ionic")
    create_figure_and_save(Ca_Bind, Mg_Bind, Na_Bind, "Binding energy", "Energy [kJ/mol]", "BindEnergy")
    
    # Looking for correlations 
    table = bind_sites()
    table["Bind_Ener_Ca"] = Ca_Bind
    table["Bind_Ener_Mg"] = Mg_Bind
    table["Bind_Ener_Na"] = Na_Bind
    table["HBond_Ca"] = Ca_HBond
    table["HBond_Mg"] = Mg_HBond
    table["HBond_Na"] = Na_HBond
    table["Ionic_Ca"] = Ca_Ionic
    table["Ionic_Mg"] = Mg_Ionic
    table["Ionic_Na"] = Na_Ionic   
    create_corr_matrix(table)

if __name__ == "__main__":
    main()
