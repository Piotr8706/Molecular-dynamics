import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def read_and_transform(f):
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
            # Add the single value to the beginning of the row and remove the last two values
            modified_row = [single_value] + list(map(float, values[:]))
            modified_data.append(modified_row)

    # Convert the modified data into a DataFrame
    return pd.DataFrame(modified_data)


def read_binden_and_analysis(typ,parameter):
    # Specify the file path
    Ca = []
    Na = []
    Mg = []
    path = r"C:\Users\piotr\Downloads\IJMS_HA+Albumin"
    match typ:
        case 'Bind':
            path = path + r"\Binding_energy"
        case 'Structural':
            path = path + r"\Structural"
        case 'H-Bond':
            path = r"C:\Users\piotr\Downloads\Results\Results\Na_HBO_1.txt"
    ends_with = r".txt"

    for i in range(1,12):
        f1 = path + r"\Ca_" + str(i) + (ends_with if typ == 'Bind' else r"_str" + ends_with)
        f2 = path + r"\Mg_" + str(i) + (ends_with if typ == 'Bind' else r"_str" + ends_with)
        f3 = path + r"\Na_" + str(i) + (ends_with if typ == 'Bind' else r"_str" + ends_with)
        # Read the data, considering the structure provided
        data1 = pd.read_table(f1, delim_whitespace=True)
        data2 = pd.read_table(f2, delim_whitespace=True)
        data3 = pd.read_table(f3, delim_whitespace=True)   
        # Select only specific columns
        Ca.append(data1[parameter][500:].mean())
        Mg.append(data2[parameter][500:].mean())
        Na.append(data3[parameter][500:].mean())
    return Ca, Mg, Na


def count_rows_with_conditions(df):
    count = {}
    
    for i in range(1, len(df)):
        # Check if the current row shares the same value in the first column as the previous row
        if df.at[i, 0] == df.at[i-1, 0] and df.at[i, 1] > 9133 and df.at[i, 2] <= 9133:
            key = df.at[i, 0]
            count[key] = count.get(key, 0) + 1
            
    return count


def main():
    f = r"C:\Users\piotr\Downloads\IJMS_HA+Albumin\Hbond\Na_HBO_2.txt"
    ga = read_and_transform(f)
    print(ga.shape)
    hbo = count_rows_with_conditions(ga)
    print(hbo)
    Ca, Mg, Na = read_binden_and_analysis('Bind','Energy')
    Ca1, Mg1, Na1 = read_binden_and_analysis('Structural','Rg_HA')

    # Display the selected data
    fig = plt.figure()
    X=np.arange(0,11)
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X + 0.00, Ca1, color = 'b', width = 0.25)
    ax.bar(X + 0.25, Mg1, color = 'g', width = 0.25)
    ax.bar(X + 0.50, Na1, color = 'r', width = 0.25)

    
    #print(graph)
    #colors = ['blue', 'orange', 'green']
    # plot histogram 
    #plt.hist([Ca, Mg, Na], bins=10, label=['Ca','Mg','Na'], alpha=0.5)
    #plt.hist(Mg, bins=50, label='Mg', alpha=0.5)
    #plt.hist(Na, bins=50, label='Na', alpha=0.5)
    #plt.legend(loc='upper right')
    #plt.hist(selected_data_4, bins=20, label='Ca', alpha=0.5)
    #plt.show()

    #f3 = plt.figure(3)
    #x = Na1
    #y = Na
    #plt.plot(x, y, 'bo')
    plt.show()
    #input()
    #correlation_coefficient = np.corrcoef(x, y)[0, 1]

    #print("Correlation coefficient:", correlation_coefficient)


if __name__=="__main__":
    main()
