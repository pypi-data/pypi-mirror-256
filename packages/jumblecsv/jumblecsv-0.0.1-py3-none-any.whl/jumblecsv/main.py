import numpy as np
import argparse


def jumble_csv(csv_file_name, *args, **kwargs):
    """ This function will jumble the csv file in "csv_file_name" as described by the *args and **kwargs

    Args:
        csv_file_name (str): Relative or absolute path to the .csv file you want to jumble. 
                             Has to be comma seperated currently

    """

                                # List of available arguments
                                # jumbling_percent = 0, 
                                # categorical_switch_probability = 0,
                                # drop_columns = [], 
                                # categorical_columns = [], 
                                # not_all_categorical_values_present = False, 
                                # block_negative = False, 
                                # number_of_header_rows = 1,
                                # output_file = "",
                                # significant_figures = 4):
                                # float_formatting = ":4.4f"
                                # int_formatting = ":4d"
    if "number_of_header_rows" in kwargs.keys():
        number_of_header_rows = kwargs["number_of_header_rows"]
    else:
        raise ValueError("The function jumble_csv was not supplied with kwarg number_of_header_rows.")


    header = np.genfromtxt(csv_file_name,delimiter=",",dtype=str)[0:number_of_header_rows,:]
    data = np.genfromtxt(csv_file_name, delimiter=",",skip_header=number_of_header_rows)
    new_data, new_header, new_categorical_columns = jumble_table(data, header, *args, **kwargs)

    output_strings = []
    current_string = ""
    longest_header_string = max([len(h) for h in new_header[0]])
    for head_row in new_header:
        for head in head_row:
            current_string += " {:{}} ,".format(head, longest_header_string)
        current_string = current_string[:-1]
        output_strings.append(current_string)
        current_string = ""
    for row in new_data:
        current_string = ""
        for i, value in enumerate(row):
            if i in new_categorical_columns:
                value = int(value)
                # Print as integer
                # First check for integer formatting
                if "int_formatting" in kwargs.keys():
                    int_formatting = kwargs["int_formatting"].replace(":","")
                    current_string += "{:{}},".format(value, int_formatting)
                    # Print as formatted int
                    continue
                default_int_fmt = " ^{}".format(2+len(new_header[0,i]))
                current_string += "{:{}},".format(value, default_int_fmt)
                continue
            # Now we are printing a float
            # First check for float formatting
            if "float_formatting" in kwargs.keys():
                # Print as float formatting
                float_formatting = kwargs["float_formatting"].replace(":","")
                current_string += "{:{}},".format(value, float_formatting)
                continue
            if "significant_figures" in kwargs.keys():
                significant_figures = int(kwargs["significant_figures"])
                sigfig_formatting = ".{}".format(significant_figures)
                current_string += "{:{}},".format(value, sigfig_formatting)
                # Print as sig figs
                continue
            default_float_fmt = " ^.{}f".format(2+len(new_header[0,i]))
            current_string += "{:{}},".format(value, default_float_fmt)
        output_strings.append(current_string[:-1])
                
            




    if "output_file" in kwargs.keys():
        output_strings[-1] += "\n"
        output_file = kwargs["output_file"]
        with open(output_file, 'w') as f:
            f.writelines(line + "\n" for line in output_strings)
        return
    else:
        for line in output_strings:
            print(line)
    

def jumble_table(data : np.ndarray, header : np.ndarray, jumbling_percent = 0.0, 
                                drop_columns = [], 
                                categorical_columns = [], 
                                not_all_categorical_values_present = False, 
                                block_negative = False,
                                categorical_switch_probability = -1.0,
                                *args, **kwargs):
    """_summary_

    Args:
        data (np.ndarray): Numpy array of shape (n,m) with all data (not headers)
        header (np.ndarray): Numpy array of shape (1,m) with all the headers (not data)
        jumbling_percent (float, optional): How many percent to shift continous parameters by. Defaults to 0.0.
        drop_columns (list, optional): Removes the columns with the selected indices from output. Defaults to [].
        categorical_columns (list, optional): List of the column indices where data is categorical. Defaults to [].
        not_all_categorical_values_present (bool, optional): Flag to indicate if not all categorical values are present. If not present, will interpolate. Defaults to False.
        block_negative (bool, optional): Removes the possibility for negative continous parameters in output. Defaults to False.
        categorical_switch_probability (float, optional): Probability in percent to change categorical parameter to other valid value. Defaults to -1.0.

    Returns:
        (tuple): Returns a tuple of (new_data, new_header, sorted_list_of_categorical_columns_in_output)
    """    
    if categorical_switch_probability == -1:
        categorical_switch_probability = jumbling_percent


    new_csv_header = header[:,]
    for i in sorted(drop_columns, reverse=True):
        new_csv_header = np.delete(new_csv_header, i, 1)
    new_csv_data   = np.zeros((data.shape[0],data.shape[1]-len(drop_columns)))


    new_categorical_columns = set()

    jj = 0
    for j in range(data.shape[1]):
        ii = 0
        if j in drop_columns:
            continue
        for i in range(data.shape[0]):
            entry = data[i,j]
            # numpy.random.rand [0,1] -> [-0.5, 0.5] -> [-1, 1] -> [-jumbling_ratio, jumbling_ratio]
            noise = (np.random.rand() - 0.5) * 2 * jumbling_percent / 100
            new_entry = entry + noise * entry
            if new_entry < 0 and block_negative:
                new_entry = 0
            if j in categorical_columns:
                new_categorical_columns.add(jj)
                data_range = np.unique(data[:,j])
                new_entry = np.random.choice( [val for val in range(int(np.min(data_range)), int(np.max(data_range)))] )

                if not not_all_categorical_values_present:
                    new_entry = np.random.choice(data_range)

                if np.random.rand() > categorical_switch_probability / 100:
                    new_entry = entry

            new_csv_data[ii,jj] = new_entry
            ii = ii + 1
        jj = jj + 1
    return new_csv_data, new_csv_header, sorted(list(new_categorical_columns))
            



                                # jumbling_percent = 0, 
                                # categorical_switch_probability = 0,
                                # drop_columns = [], 
                                # categorical_columns = [], 
                                # not_all_categorical_values_present = False, 

                                # block_negative = False, 
                                # number_of_header_rows = 1,
                                # output_file = "",
                                # significant_figures = 4):
                                # float_formatting = ":4.4f"
                                # int_formatting = ":4d"


# if __name__=="__main__":
def main():
    parser = argparse.ArgumentParser(description='Tool for jumbling data, removing data and reformatting data in CSV format.')
    parser.add_argument('-p','--jumbling-percent', type=int, required=False, default=0, \
                help='Percentage to jumble non-categorical values in %%') 
    parser.add_argument('-c','--categorical-switch-probability', type=int, required=False, default=0,\
                help='Probability to change a categorical parameter in %%')
    parser.add_argument('-d','--drop-columns', type=int, nargs='*', required=False,\
                help='List of column indices to drop in the new table') 
    parser.add_argument('-l', '--categorical-columns', type=int, nargs='*', required=False,\
                help='List of column indices containing a categorical parameter')
    parser.add_argument('-o','--output-file', type=str, required=False,\
                help='Write the resulting CSV file to this path')
    
    parser.add_argument('--not-all-categorical-parameters-present', action='store_true', required=False,\
                help='Set this if all possible values of categorical parameters are not present in the data. If set\
                        data will be interpolated, so we assume the outer values are represented.')
    parser.add_argument('--block-negative', action='store_true', required=False,\
                help='Caps values at a minimum of 0')
    parser.add_argument('-n','--number-of-header-rows', type=int, required=False, default=1,\
                help='Number of header rows in the input CSV file')

    parser.add_argument('--significant-figures', type=int, required=False,\
                help='Number of significant figures to use when printing floats.\
                    If neither \'--significant-figures\', \'--float-formatting\'\
                        is set, the values will be represented centrally, as wide as the header of the column')    
    parser.add_argument('--float-formatting', type=str, required=False,\
                help='Float formatting to use when printing. E.g. \'4.2f\', \' ^8.2f\'.\
                    Whatever is accepted by your python interpreter \'print\' function should work.')    
    parser.add_argument('--int-formatting', type=str, required=False,\
                help='Integer formatting to use when printing. E.g. \'4d\', \' ^8d\'.\
                    Whatever is accepted by your python interpreter \'print\' function should work.\
                        If not set the values will be represented centrally, as wide as the header of the column')  
    
    parser.add_argument('csv_file_path', metavar='csv_path', type=str,
                    help='Path to the .csv file. Note the file has to be comma seperated with full-stop decimals\
                        , not semicolon with comma decimal.')
                    
        
                
    args = parser.parse_args()

    csv_file_path = args.csv_file_path
    number_of_header_rows = args.number_of_header_rows


    kwargs = vars(args)
    kwargs = {k:v for k,v in kwargs.items() if v is not None}
    jumble_csv(csv_file_path, **kwargs)