import pandas as pd

# Load the Excel file and the specific sheet
input_file = "data.xlsx"
sheet_name = "12. Data"

# Read the sheet, skipping the first 5 rows
df = pd.read_excel(input_file, sheet_name=sheet_name, skiprows=5)

# Save the cleaned data to a new Excel file
output_file = "data_no_first5.xlsx"
df.to_excel(output_file, index=False)

print(f"First 5 rows removed and saved to {output_file}")

# Load the Excel file
input_file = "data_no_first5.xlsx"  # Update this path if needed
df = pd.read_excel(input_file)

# Step 1: Drop unnamed columns (e.g., 'Unnamed: 0', etc.)
df_clean = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Step 2: Drop columns 11 to 52 (i.e., index 10 to 51)
cols_to_drop = df_clean.columns[10:52]
df_cleaned = df_clean.drop(columns=cols_to_drop)

# Step 3: Save to a new Excel file
output_file = "data_columns_11_to_52_removed.xlsx"
df_cleaned.to_excel(output_file, index=False)

print(f"Columns 11 to 52 removed. Cleaned file saved to: {output_file}")


# Load the Excel file
input_file = "data_columns_11_to_52_removed.xlsx"  # Adjust path as needed
df = pd.read_excel(input_file)

# Drop unnamed columns
df_clean = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Step 1: Identify columns 4 to 10 (index 3 to 9)
cols_to_merge = df_clean.columns[3:10]

# Step 2: Merge their content into 'DESCRIPTION' (concatenate non-null values with spaces)
df_clean["DESCRIPTION"] = df_clean[cols_to_merge] \
    .apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1) \
    .str.replace(r'\bnan\b', '', regex=True) \
    .str.replace(r'\s+', ' ', regex=True).str.strip()
# Step 3: Drop columns 4 to 10 (they've been merged into DESCRIPTION now)
df_clean = df_clean.drop(columns=cols_to_merge)

df.iloc[1] = range(1, len(df.columns) + 1)

# Step 4: Save to a new file
output_file = "data_description_merged.xlsx"
df_clean.to_excel(output_file, index=False)

print(f"Columns 4-10 merged into 'DESCRIPTION' and saved to: {output_file}")


# Load your processed file
input_file = "data_description_merged.xlsx"
df = pd.read_excel(input_file, header=None)  # Use header=None to treat all rows as data

# Overwrite row 2 (index 1) with sequential numbers
df.iloc[1, :] = range(1, len(df.columns) + 1)
df_trimmed = df.iloc[:82]

# Save the result
output_file = "data_row2_fixed.xlsx"
df_trimmed.to_excel(output_file, index=False, header=False)

print(f"Row 2 numbering fixed and saved to {output_file}")

