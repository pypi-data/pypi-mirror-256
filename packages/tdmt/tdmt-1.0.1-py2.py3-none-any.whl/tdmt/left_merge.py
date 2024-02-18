import pandas as pd
from pandas import DataFrame
try:
    import utils
    from decorators import validate_ref
except:
    from . import utils
    from .decorators import validate_ref


@validate_ref
def left_merge(
    input_data_tables: dict, workflow_map: dict, ref: str, log: DataFrame
) -> dict:
    """
    Left merge one DataFrame with another based on common key columns, ensuring data integrity by
    excluding records with blank key values and handling duplicates appropriately.

    Parameters:
    - input_data_tables: A dictionary of DataFrames to merge. The first entry is the left hand side and the second entry is the right hand one.
    - workflow_map: A dictionary representing the workflow map, a spreadsheet detailing data processing steps.
    - ref: A string specifying the columns to use for matching records.
    - log: A DataFrame for logging operation messages and errors.

    Returns:
    A dictionary containing 'dataframe' with the result of the key transfer, 'ErrorFrame' capturing any records
    involved in duplicate key issues, and 'OK_to_continue' indicating whether the operation was successful.
    """

    # Initialize return object for error cases
    
    ErrorFrame=pd.DataFrame()
    
    ReturnOnError = {
        "dataframe": pd.DataFrame(),
        "ErrorFrame": pd.DataFrame(),
        "OK_to_continue": False,
    }

    # Ensure exactly two input DataFrames are provided
    input_keys_list = list(input_data_tables.keys())
    if len(input_keys_list) != 2:
        utils.print_and_log_message(
            {
                "message": f"Operation transfer_key requires exactly 2 input dataframes: {', '.join(input_keys_list)}"
            },
            log,
        )
        return ReturnOnError

    # Extract the DataFrames for operation
    left_dataframe, right_dataframe = [
        input_data_tables[key].reset_index(drop=True) for key in input_keys_list
    ]

    # Parse the reference to identify the key to transfer and the existing keys in common
    existing_keys_in_common = ref.split(",")
    
    if not set(existing_keys_in_common).issubset(left_dataframe.columns):
        missing_columns=list(set(existing_keys_in_common)-set(left_dataframe.columns))
        utils.print_and_log_message(
            {
                "message": f"Operation left_merge needs to merge on columns: {', '.join(existing_keys_in_common)} but some are missing from the left dataframe: {', '.join(missing_columns)}"
            },
            log,
        )
        return ReturnOnError

    if not set(existing_keys_in_common).issubset(right_dataframe.columns):
        missing_columns=list(set(existing_keys_in_common)-set(right_dataframe.columns))
        utils.print_and_log_message(
            {
                "message": f"Operation left_merge needs to merge on columns: {', '.join(existing_keys_in_common)} but some are missing from the right dataframe: {', '.join(missing_columns)}"
            },
            log,
        )
        return ReturnOnError
    
    # Filter out records with blanks in the keys from the right DataFrame
    has_blanks_in_keys = left_dataframe[existing_keys_in_common].isnull().any(axis=1)
    left_dataframe_with_blank_keys, left_dataframe_nonblank_keys = (
        left_dataframe[has_blanks_in_keys],
        left_dataframe[~has_blanks_in_keys],
    )

    # Perform the merge operation to transfer the key, excluding records with blank keys
    merged_dataframe = pd.merge(left_dataframe_nonblank_keys,right_dataframe,
        on=existing_keys_in_common,
        how="left",
    )

    # Combine the merged DataFrames and reset the index
    dataframe = (
        pd.concat([merged_dataframe, left_dataframe_with_blank_keys], ignore_index=True)
        .sort_values(by=existing_keys_in_common)
        .reset_index(drop=True)
    )

    return {"dataframe": dataframe, "ErrorFrame": ErrorFrame, "OK_to_continue": True}
