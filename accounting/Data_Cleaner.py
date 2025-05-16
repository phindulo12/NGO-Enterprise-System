import pandas as pd
from datetime import datetime
import re


def import_excel_to_django_format(file_path):
    try:
        # Read the Excel file with header=None to manually process headers
        df_raw = pd.read_excel(file_path, sheet_name='12. Data', header=None, engine='openpyxl')
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return None

    # ===== 1. Extract and Process Headers =====
    # The actual data starts at row 7 (0-indexed)
    headers = df_raw.iloc[3:7, :]  # Get header rows (rows 4-7)

    # Combine headers into single column names
    combined_headers = []
    for col in range(headers.shape[1]):
        parts = []
        for row in range(headers.shape[0]):
            cell_value = headers.iloc[row, col]
            if pd.notna(cell_value) and str(cell_value).strip() != '':
                parts.append(str(cell_value).strip())
        combined_headers.append('_'.join(parts).upper().replace(' ', '_'))

    # Set the combined headers and remove header rows
    df = df_raw.iloc[7:, :]  # Data starts at row 8
    df.columns = combined_headers

    # ===== 2. Identify Core Columns =====
    # These columns appear to be static based on the Excel structure
    core_columns = {
        'BUDGET_LINE': None,
        'SDA': None,
        'DESCRIPTION': None,
        'COST_CATEGORY': None
    }

    # Find the actual column names that match our core columns
    for col in df.columns:
        col_clean = re.sub(r'[_\s]', '', col.upper())
        if 'BUDGETLINE' in col_clean:
            core_columns['BUDGET_LINE'] = col
        elif 'SDA' in col_clean:
            core_columns['SDA'] = col
        elif 'DESCRIPTION' in col_clean:
            core_columns['DESCRIPTION'] = col
        elif 'COSTCATEGORY' in col_clean:
            core_columns['COST_CATEGORY'] = col

    # Check if we found all required columns
    missing = [k for k, v in core_columns.items() if v is None]
    if missing:
        print(f"❌ Missing required columns: {missing}")
        return None

    # ===== 3. Process Time Period Columns =====
    # Extract month information from row 4 (0-indexed)
    month_info = df_raw.iloc[3, :].values

    # Create a list of all time periods with their month numbers
    time_periods = []
    for i, val in enumerate(month_info):
        if pd.notna(val) and str(val).strip() != '':
            try:
                month_num = int(val)
                time_periods.append((i, month_num))
            except ValueError:
                pass

    # ===== 4. Reshape Data =====
    melted_data = []

    for idx, row in df.iterrows():
        for col_idx, month_num in time_periods:
            col_name = df.columns[col_idx]

            # Skip core columns
            if col_name in core_columns.values():
                continue

            # Determine metric type (BUDGET, ACTUAL, or VARIANCE)
            metric_type = None
            if 'BUDGET' in col_name.upper():
                metric_type = 'BUDGET'
            elif 'ACTUAL' in col_name.upper():
                metric_type = 'ACTUAL'
            elif 'VARIANCE' in col_name.upper():
                metric_type = 'VARIANCE'

            if metric_type:
                # Create a date (using current year + month from the data)
                year = datetime.now().year
                date = datetime(year, month_num, 1).strftime('%Y-%m-%d')

                record = {
                    'BUDGET_LINE': row[core_columns['BUDGET_LINE']],
                    'SDA': row[core_columns['SDA']],
                    'DESCRIPTION': row[core_columns['DESCRIPTION']],
                    'COST_CATEGORY': row[core_columns['COST_CATEGORY']],
                    'DATE': date,
                    'MONTH': month_num,
                    'QUARTER': (month_num - 1) // 3 + 1,
                    'METRIC': metric_type,
                    'VALUE': row[col_name]
                }

                melted_data.append(record)

    # Create DataFrame from melted data
    df_melted = pd.DataFrame(melted_data)

    # Pivot to get BUDGET, ACTUAL, VARIANCE as columns
    final_df = df_melted.pivot_table(
        index=['BUDGET_LINE', 'SDA', 'DESCRIPTION', 'COST_CATEGORY', 'DATE', 'MONTH', 'QUARTER'],
        columns='METRIC',
        values='VALUE',
        aggfunc='first'
    ).reset_index()

    # Clean up column names
    final_df.columns.name = None
    final_df = final_df.rename(columns={
        'BUDGET': 'BUDGET',
        'ACTUAL': 'ACTUAL',
        'VARIANCE': 'VARIENCE'
    })

    # Add month calendar field
    final_df['MONTH_CALENDER'] = pd.to_datetime(final_df['DATE']).dt.strftime('%Y-%m-%d')

    # Reorder columns
    column_order = [
        'QUARTER', 'MONTH', 'MONTH_CALENDER', 'BUDGET_LINE', 'SDA',
        'DESCRIPTION', 'COST_CATEGORY', 'BUDGET', 'ACTUAL', 'VARIENCE'
    ]

    return final_df[column_order].fillna(0)


# Test the function
if __name__ == "__main__":
    formatted_df = import_excel_to_django_format('data.xlsx')

    if formatted_df is not None:
        print("✅ Successfully transformed data:")
        print(formatted_df.head())
        formatted_df.to_csv("cleaned_budget_data.csv", index=False)
    else:
        print("❌ Failed to process Excel file.")

