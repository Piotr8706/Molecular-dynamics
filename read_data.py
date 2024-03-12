import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time

# TODO: rename module Read_data.py to read_data.py - do not use Upper letters - done
# TODO: Add some typing and 
# TODO: in next two month you don't forget about what 'f' is.- done
# TODO: improve 'f' variable name - done
# TODO: good practice is add Arguments: and Returns: in docstring
# TODO: add below lines to docstring

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
    # TODO: Read about pd.read_csv(), pd.read_table() and load file direct to pd.DataFrame()
    with open(file, "r") as file:
        lines = file.readlines()

    # Initialize empty lists to store modified data
    modified_data = []

    # Iterate through the lines
    # TODO: make less iterations each elements use operations of DataFrames to change datasets
    for line in lines:
        # Split the line by whitespaces
        values = line.strip().split()

        # If the line contains a single value
        if len(values) == 1:
            # TODO: this value should not be return in DataFrame
            # TODO: or single_value could be a index and data could be a pd.Series inside pd.DataFrame
            # TODO: make answer for question - for what will be single_value use?
            timestamp = float(values[0])
        else:
            # Add the single value to the beginning of the row
            # TODO: make convert to float for column used pandas manipulation functions
            modified_row = [timestamp] + list(map(float, values[:]))
            modified_data.append(modified_row)

    # Convert the modified data into a DataFrame
    # TODO: change return
    #   return pd.DataFrame(modified_data), single_value
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
            """
            an example for unpack function returns:
            
            f1_data, f1_start_number = read_and_transform(f1)
            data1 = count_rows_with_conditions(f1_data)
            """
            data1 = count_rows_with_conditions(read_and_transform(f1))
            data2 = count_rows_with_conditions(read_and_transform(f2))
            data3 = count_rows_with_conditions(read_and_transform(f3))
            # TODO: data1.mean()
            Ca.append(sum(data1.values()) / len(data1))
            Mg.append(sum(data2.values()) / len(data2))
            Na.append(sum(data3.values()) / len(data3))
    return Ca, Mg, Na


def count_rows_with_conditions(df):
    """Counts number of interactions in time stamp. However we are only interested in 
    intermolecular interactions so that certain conditions must be applied"""
    
    # TODO: make filtered_df based on df and select methods from pandas
    # TODO: remove for use filtered_df.count()
    filtered_df = df[(df.iloc[:, 1] < 9133) & (df.iloc[:, 2] >= 9133) & (df.iloc[:, 1] < 10240) & (df.iloc[:, 2] < 10240)]
    if filtered_df.empty:
        return {}
    count = filtered_df.groupby('Timestamp').size().to_dict()

    return count

def create_figure_and_save():
    Ca1, Mg1, Na1 = read_file_show_interaction('HBond', '')
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

    
def main():
    # TODO: make function from code below
    # Display the selected data
    start = time.time()
    create_figure_and_save()
    end = time.time()
    print(end-start)
if __name__ == "__main__":
    main()