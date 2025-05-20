import pandas as pd
import os

def clean_excel_data(input_file):
    # Ensure the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")
    
    base_dir = os.path.dirname(input_file)

    # Step 1: Read Excel file and skip first 5 rows
    sheet_name = "12. Data"
    df = pd.read_excel(input_file, sheet_name=sheet_name, skiprows=5, engine='openpyxl')
    temp_file1 = os.path.join(base_dir, "data_no_first5.xlsx")
    df.to_excel(temp_file1, index=False)
    print(f"First 5 rows removed and saved to {temp_file1}")

    # Step 2: Remove unnamed columns and drop columns 11 to 52
    df = pd.read_excel(temp_file1)
    df_clean = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    cols_to_drop = df_clean.columns[10:52]
    df_cleaned = df_clean.drop(columns=cols_to_drop)
    temp_file2 = os.path.join(base_dir, "data_columns_11_to_52_removed.xlsx")
    df_cleaned.to_excel(temp_file2, index=False)
    print(f"Columns 11 to 52 removed. Cleaned file saved to: {temp_file2}")

    # Step 3: Merge columns 4 to 10 into 'DESCRIPTION'
    df = pd.read_excel(temp_file2)
    df_clean = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    cols_to_merge = df_clean.columns[3:10]
    df_clean["DESCRIPTION"] = df_clean[cols_to_merge] \
        .apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1) \
        .str.replace(r'\bnan\b', '', regex=True) \
        .str.replace(r'\s+', ' ', regex=True).str.strip()
    df_clean = df_clean.drop(columns=cols_to_merge)
    temp_file3 = os.path.join(base_dir, "data_description_merged.xlsx")
    df_clean.to_excel(temp_file3, index=False)
    print(f"Columns 4-10 merged into 'DESCRIPTION' and saved to: {temp_file3}")

    # Step 4: Fix row 2 values and trim to 82 rows
    df = pd.read_excel(temp_file3, header=None)
    df.iloc[1, :] = range(1, len(df.columns) + 1)
    df_trimmed = df.iloc[:82]
    final_output_file = os.path.join(base_dir, "data_row2_fixed.xlsx")
    df_trimmed.to_excel(final_output_file, index=False, header=False)
    print(f"Row 2 numbering fixed and saved to {final_output_file}")
    
    return final_output_file  # Returning the final output file path

# Example usage:
# result_file = clean_excel_data(r"C:\path\to\data.xlsx")


