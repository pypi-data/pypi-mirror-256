# Tabular Data Management Tool (tdmt)

## Documetation
To follow along with the examples please find the templates in the gitlab repo. 

- Open the spreadsheet corresponding to the example operation. For example, for add_key, open example_add_key.xlsx
- Check the raw tab to see which files from the input directory it loads. Open the relevant input files to see what they look like.
- Check the out tab to see what files it will write to the output directory. 
- Run the example using the one of the commands provided, depending on whether you installed the package or cloned the repo.
- Check the output directory, open the newly created files and verify how the input files were processed.
- Also check out the log for an audit trail of every step performed.

## skeleton mode
tdmt example_skeleton1

python3 tdmt.py example_skeleton1

tdmt example_skeleton2

python3 tdmt.py example_skeleton2

Automates the preparation of a workflow map spreadsheet based on provided data. This includes generating run lists for mapping and renaming operations, creating reference tables for mappings, and summarizing data for mapped columns. The results are saved as Excel files in the specified output directory.

## add_key
tdmt example_add_key

python3 tdmt.py example_add_key

Adds a unique identifier to the input DataFrame based on a reference string.

## concat
tdmt example_concat

python3 tdmt.py example_concat

Concatenates multiple DataFrames into a single DataFrame.

## filter_rows
tdmt example_filter_rows

python3 tdmt.py example_filter_rows

Filters rows in a DataFrame based on filter criteria specified in the workflow map spreadsheet.

## format_dates
tdmt example_format_dates

python3 tdmt.py example_format_dates

Formats the date columns of a DataFrame based on the format strings specified in the workflow map spreadsheet.

## groupstats
tdmt example_groupstats

python3 tdmt.py example_groupstats

Applies group-based statistical operations to a DataFrame and generates a new column with the results.

## hardcode_column
tdmt example_hardcode_column

python3 tdmt.py example_hardcode_column

Adds or replaces a column in the DataFrame with a hardcoded value. 

## left_merge
tdmt example_left_merge

python3 tdmt.py example_left_merge

Left merge one DataFrame with another based on common key columns, ensuring data integrity by excluding records with blank key values and handling duplicates appropriately.

## map_and_rename
tdmt example_map_and_rename1

python3 tdmt.py example_map_and_rename1

tdmt example_map_and_rename2

python3 tdmt.py example_map_and_rename2

Maps and renames columns in a DataFrame based on specifications from a workflow map spreadsheet. This function allows for values within specified columns to be replaced according to a mapping table and for columns to be renamed. The function supports keeping original columns and handling mapping exceptions according to global settings.

## multicolmap
tdmt example_multicolmap

python3 tdmt.py example_multicolmap

Maps values from multiple columns in the input DataFrame to a new column based on mappings defined in a workflow map spreadsheet. The function requires a reference table with mappings and the name for the new column, which should be the last column in the reference table. If the new column name already exists in the input DataFrame, it will be overwritten.

## transfer_key
tdmt example_transfer_key

python3 tdmt.py example_transfer_key

Transfers a specified key from one DataFrame to another based on common key columns, ensuring data integrity by excluding records with blank key values and handling duplicates appropriately.

## unmerge
tdmt example_unmerge

python3 tdmt.py example_unmerge

Separates a specified subset from a larger DataFrame based on defined keys and other columns, identifying conflicts. 

## unstack
tdmt example_unstack

python3 tdmt.py example_unstack

Transforms specified columns of a DataFrame into rows, creating a new key for unique identification and ignoring blanks. This operation targets scenarios where data representation benefits from pivoting columns to rows for enhanced analysis.