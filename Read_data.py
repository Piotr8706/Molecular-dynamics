import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def read_and_transform(f):
    """This project deals with three different type of file structure. The purpose of 
    this function is to read files with H-bonds and ionic interations which have following structure:
    40000000.000
    1.000 852.000 14.775 0 4.000 2.180
    8.000 55.000 25.000 1 56.000 1.996
    12.000 898.000 22.275 0 13.000 1.624
    19.000 73.000 25.000 1 74.000 1.804
    34.000 97.000 17.775 1 98.000 1.850
    50.000 117.000 16.600 1 118.000 2.268
    It starts with timestamp followed by list of all interactions of given type.
    Function puts time stamp in first column"""
    with open(f, "r") as file:
        lines = file.readlines()

    # Initialize empty lists to store modified data
    modified_data = []
    single_value = None

    # Iterate through the lines
    for line in lines:
        # Split the line by whitespaces
        values = line.strip().split()

        # If the line contains a single value
        if len(values) == 1:
            single_value = float(values[0])
        else:
            # Add the single value to the beginning of the row
            modified_row = [single_value] + list(map(float, values[:]))
            modified_data.append(modified_row)

    # Convert the modified data into a DataFrame
    return pd.DataFrame(modified_data)


def read_file_show_interaction(typ,parameter):
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
   
    for i in range(1,13):
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
            data1 = count_rows_with_conditions(read_and_transform(f1))
            data2 = count_rows_with_conditions(read_and_transform(f2))
            data3 = count_rows_with_conditions(read_and_transform(f3))
            Ca.append(sum(data1.values()) / len(data1))
            Mg.append(sum(data2.values()) / len(data2))
            Na.append(sum(data3.values()) / len(data3))        
    return Ca, Mg, Na


def count_rows_with_conditions(df):
    """Counts number of interactions in time stamp. However we are only interested in 
    intermolecular interactions so that certain conditions must be applied"""
    count = {}
    for i in range(1, len(df)):
        # Check if the current row shares the same value in the first column as the previous row
        if df.at[i, 0] == df.at[i-1, 0] and df.at[i, 1] < 9133 and df.at[i, 2] >= 9133 and df.at[i, 1] < 10240 and df.at[i, 2] < 10240:
            key = df.at[i, 0]
            count[key] = count.get(key, 0) + 1
            
    return count


def main():

    Ca1, Mg1, Na1 = read_file_show_interaction('HBond','')

    # Display the selected data
    fig = plt.figure()
    X = np.arange(0, 12)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(X + 0.00, Ca1, color='b', width=0.25, label='Ca')
    ax.bar(X + 0.25, Mg1, color='g', width=0.25, label='Mg')
    ax.bar(X + 0.50, Na1, color='r', width=0.25, label='Na')
    ax.set_title("Hydrogen Bonds")
    ax.set_xlabel("Site")  # Added x-axis label
    ax.set_ylabel("# of H-bonds")
    plt.legend(loc='upper right')
    plt.savefig('./Files/HBonds_vs_site.png')
    plt.show()  


if __name__=="__main__":
    main()
