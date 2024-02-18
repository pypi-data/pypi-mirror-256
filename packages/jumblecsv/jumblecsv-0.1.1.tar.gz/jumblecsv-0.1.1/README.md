usage: main.py [-h] [-p JUMBLING_PERCENT] [-c CATEGORICAL_SWITCH_PROBABILITY]
               [-d [DROP_COLUMNS ...]] [-l [CATEGORICAL_COLUMNS ...]]
               [-o OUTPUT_FILE] [--not-all-categorical-parameters-present]
               [--block-negative] [-n NUMBER_OF_HEADER_ROWS]
               [--significant-figures SIGNIFICANT_FIGURES]
               [--float-formatting FLOAT_FORMATTING]
               [--int-formatting INT_FORMATTING]
               csv_path

Tool for jumbling data, removing data and reformatting data in CSV format.

positional arguments:
  csv_path              Path to the .csv file. Note the file has to be comma
                        seperated with full-stop decimals , not semicolon with
                        comma decimal.

options:
  -h, --help            show this help message and exit
  -p JUMBLING_PERCENT, --jumbling-percent JUMBLING_PERCENT
                        Percentage to jumble non-categorical values in %
  -c CATEGORICAL_SWITCH_PROBABILITY, --categorical-switch-probability CATEGORICAL_SWITCH_PROBABILITY
                        Probability to change a categorical parameter in %
  -d [DROP_COLUMNS ...], --drop-columns [DROP_COLUMNS ...]
                        List of column indices to drop in the new table
  -l [CATEGORICAL_COLUMNS ...], --categorical-columns [CATEGORICAL_COLUMNS ...]
                        List of column indices containing a categorical
                        parameter
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Write the resulting CSV file to this path
  --not-all-categorical-parameters-present
                        Set this if all possible values of categorical
                        parameters are not present in the data. If set data
                        will be interpolated, so we assume the outer values
                        are represented.
  --block-negative      Caps values at a minimum of 0
  -n NUMBER_OF_HEADER_ROWS, --number-of-header-rows NUMBER_OF_HEADER_ROWS
                        Number of header rows in the input CSV file
  --significant-figures SIGNIFICANT_FIGURES
                        Number of significant figures to use when printing
                        floats. If neither '--significant-figures', '--float-
                        formatting' is set, the values will be represented
                        centrally, as wide as the header of the column
  --float-formatting FLOAT_FORMATTING
                        Float formatting to use when printing. E.g. '4.2f', '
                        ^8.2f'. Whatever is accepted by your python
                        interpreter 'print' function should work.
  --int-formatting INT_FORMATTING
                        Integer formatting to use when printing. E.g. '4d', '
                        ^8d'. Whatever is accepted by your python interpreter
                        'print' function should work. If not set the values
                        will be represented centrally, as wide as the header
                        of the column
