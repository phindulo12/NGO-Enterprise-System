import re

import pandas as pd
from datetime import datetime


def import_excel_to_django_format(file_path):
    # Load raw data with multi-index headers
    try:
        df_raw = pd.read_excel(
            file_path,
            sheet_name='12. Data',
            header=[0, 1, 2, 3, 4],
            engine='openpyxl'
        )
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return None

    # ===== 1. Flatten Column Headers =====
    flattened_cols = []
    for col in df_raw.columns:
        if isinstance(col, tuple):
            clean_parts = []
            for part in col:
                str_part = str(part).strip()
                if str_part.startswith('Unnamed') or not str_part:
                    continue
                if isinstance(part, datetime):
                    clean_parts.append(part.strftime('%Y-%m-%d'))
                else:
                    clean_parts.append(str_part.replace(' ', '_').upper())
            clean_name = '_'.join(clean_parts)
        else:
            clean_name = str(col).strip().replace(' ', '_').upper()

        if not clean_name:
            clean_name = "UNKNOWN"
        suffix = 1
        original_name = clean_name
        while clean_name in flattened_cols:
            clean_name = f"{original_name}_{suffix}"
            suffix += 1

        flattened_cols.append(clean_name)

    df_raw.columns = flattened_cols
    print("🛠️ Flattened columns:", flattened_cols)  # ADD THIS LINE

    # ===== 2. Normalize Core Field Names =====
    # Map variations to canonical names expected by Django# Updated header mapping section
    header_map = {
        'BUDGET_LINE': [
            'BUDGET_LINE', 'BUDGETLINE', 'LINE_ITEM', 'LINE_NO',
            'BUDGET LINE', 'Budget Line', 'LINE_ITEM_NO'
        ],
        'SDA': [
            'SDA', 'SUB_PROGRAM', 'SUB_PROGRAMME',
            'PROGRAM_AREA', 'DISTRICT', 'REGION'
        ],
        'DESCRIPTION': [
            'DESCRIPTION', 'DESC', 'ACTIVITY_DESCRIPTION',
            'LINE_DESCRIPTION', 'ACTIVITY'
        ],
        'COST_CATEGORY': [
            'COST_CATEGORY', 'CATEGORY', 'COST_CAT',
            'EXPENSE_TYPE', 'BUDGET_CATEGORY', 'COST_TYPE'
        ],
    }

    # Updated column renaming logic
    col_renames = {}
    for canonical, aliases in header_map.items():
        for alias in aliases:
            for col in df_raw.columns:
                # Normalize both sides for comparison
                norm_col = re.sub(r'[_\s-]', '', col.upper())
                norm_alias = re.sub(r'[_\s-]', '', alias.upper())

                if norm_col == norm_alias:
                    col_renames[col] = canonical
                    break
    df_raw = df_raw.rename(columns=col_renames)

    # ===== 3. Check for Required Columns =====
    required_columns = {'BUDGET_LINE', 'SDA', 'DESCRIPTION', 'COST_CATEGORY'}
    print("🧾 Available columns:", df_raw.columns.tolist())
    missing = required_columns - set(df_raw.columns)
    if missing:
        print(f"❌ Missing required columns: {missing}")
        return None

    # ===== 4. Melt Data into Long Format =====
    metric_cols = [
        col for col in df_raw.columns
        if any(col.startswith(prefix) for prefix in ['BUDGET_', 'ACTUAL_', 'VARIANCE_'])
    ]

    try:
        df_melted = df_raw.melt(
            id_vars=['BUDGET_LINE', 'SDA', 'DESCRIPTION', 'COST_CATEGORY'],
            value_vars=metric_cols,
            var_name='METRIC_DATE',
            value_name='VALUE'
        )
    except KeyError as e:
        print(f"❌ Column error during melt: {str(e)}")
        return None

    # ===== 5. Split Metric and Date =====
    split_regex = r'(BUDGET|ACTUAL|VARIANCE)_(\d{4}-\d{2}-\d{2})'
    splits = df_melted['METRIC_DATE'].str.extract(split_regex)

    if splits.shape[1] != 2:
        print("❌ Failed to split METRIC_DATE column into Metric and Date")
        return None

    df_melted['METRIC'] = splits[0]
    df_melted['DATE'] = pd.to_datetime(splits[1], errors='coerce')
    df_melted = df_melted.drop(columns=['METRIC_DATE'])
    df_melted['VALUE'] = pd.to_numeric(df_melted['VALUE'], errors='coerce')

    # Forward-fill core metadata
    for col in ['SDA', 'DESCRIPTION', 'COST_CATEGORY']:
        df_melted[col] = df_melted[col].ffill()

    # ===== 6. Pivot to Final Format =====
    try:
        final_df = df_melted.pivot_table(
            index=['BUDGET_LINE', 'SDA', 'DESCRIPTION', 'COST_CATEGORY', 'DATE'],
            columns='METRIC',
            values='VALUE',
            aggfunc='first'
        ).reset_index()
    except Exception as e:
        print(f"❌ Pivot error: {str(e)}")
        return None

    # Clean column names and add time breakdowns
    final_df.columns.name = None
    final_df.columns = [col.upper() for col in final_df.columns]

    final_df = final_df.rename(columns={
        'BUDGET': 'BUDGET',
        'ACTUAL': 'ACTUAL',
        'VARIANCE': 'VARIENCE'
    })

    final_df['QUARTER'] = final_df['DATE'].dt.quarter
    final_df['MONTH'] = final_df['DATE'].dt.month
    final_df['MONTH_CALENDER'] = final_df['DATE'].dt.strftime('%Y-%m-%d')

    # Reorder to match Django model
    column_order = [
        'QUARTER', 'MONTH', 'MONTH_CALENDER', 'BUDGET_LINE', 'SDA',
        'DESCRIPTION', 'COST_CATEGORY', 'BUDGET', 'ACTUAL', 'VARIENCE'
    ]

    return final_df[column_order].fillna(0)


# ======================= ✅ TEST ========================
if __name__ == "__main__":
    formatted_df = import_excel_to_django_format('data.xlsx')

    if formatted_df is not None:
        print("✅ Successfully transformed data:")
        print(formatted_df.head())

        # Optional: Save preview to CSV
        formatted_df.to_csv("cleaned_budget_data.csv", index=False)

        # Django insert example:
        # from yourapp.models import Data
        # for index, row in formatted_df.iterrows():
        #     Data.objects.create(
        #         Quarter=row['QUARTER'],
        #         Month=row['MONTH'],
        #         Month_calender=row['MONTH_CALENDER'],
        #         Budget_Line=row['BUDGET_LINE'],
        #         SDA=row['SDA'],
        #         description=row['DESCRIPTION'],
        #         Cost_Category=row['COST_CATEGORY'],
        #         Budget=row['BUDGET'],
        #         Actual=row['ACTUAL'],
        #         Varience=row['VARIENCE']
        #     )
    else:
        print("❌ Failed to process Excel file.")

