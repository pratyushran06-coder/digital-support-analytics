import pandas as pd
import numpy as np
from pathlib import Path
import os

def main():
    # Setup paths
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
    PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_support_tickets_clean.csv"
    REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

    # Ensure directories exist
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("1. LOAD DATA")
    print("==================================================")
    df = pd.read_csv(RAW_DATA_PATH)
    original_row_count = len(df)
    print(f"Shape: {df.shape}")
    print("Column names:\n", df.columns.tolist())
    print("\nData types:\n", df.dtypes)

    print("\n==================================================")
    print("2. STANDARDIZE COLUMN NAMES")
    print("==================================================")
    col_mapping = {
        'Ticket ID': 'ticket_id',
        'Customer Name': 'customer_name',
        'Customer Email': 'customer_email',
        'Customer Age': 'customer_age',
        'Customer Gender': 'customer_gender',
        'Product Purchased': 'product_purchased',
        'Date of Purchase': 'date_of_purchase',
        'Ticket Type': 'ticket_type',
        'Ticket Subject': 'ticket_subject',
        'Ticket Description': 'ticket_description',
        'Ticket Status': 'ticket_status',
        'Resolution': 'resolution',
        'Ticket Priority': 'ticket_priority',
        'Ticket Channel': 'ticket_channel',
        'First Response Time': 'first_response_time',
        'Time to Resolution': 'time_to_resolution',
        'Customer Satisfaction Rating': 'csat'
    }
    df.rename(columns=col_mapping, inplace=True)
    print("Columns standardized.")

    print("\n==================================================")
    print("3. REMOVE DUPLICATE ROWS")
    print("==================================================")
    duplicate_count_before = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    duplicate_count_removed = duplicate_count_before
    rows_remaining = len(df)
    print(f"Duplicate count before cleaning: {duplicate_count_before}")
    print(f"Duplicate count removed: {duplicate_count_removed}")
    print(f"Rows remaining: {rows_remaining}")

    print("\n==================================================")
    print("4. TICKET ID")
    print("==================================================")
    df['ticket_id'] = pd.to_numeric(df['ticket_id'], errors='coerce')
    dup_ids = df.duplicated(subset=['ticket_id']).sum()
    print(f"Duplicate ticket IDs: {dup_ids}")

    print("\n==================================================")
    print("5. TEXT CLEANING")
    print("==================================================")
    text_cols = [
        'customer_name', 'customer_email', 'customer_gender', 'product_purchased',
        'ticket_type', 'ticket_subject', 'ticket_description', 'ticket_status',
        'resolution', 'ticket_priority', 'ticket_channel'
    ]
    for col in text_cols:
        if col in df.columns:
            # Strip whitespace, treat empty strings as NaN for categorical logic later (though prompt says whitespace cleaning only)
            # "Perform only safe whitespace cleaning: strip leading/trailing whitespace"
            mask = df[col].notna()
            df.loc[mask, col] = df.loc[mask, col].astype(str).str.strip()
    print("Text columns stripped.")

    print("\n==================================================")
    print("6. DATE CLEANING")
    print("==================================================")
    dates_before = df['date_of_purchase'].notna().sum()
    df['date_of_purchase'] = pd.to_datetime(df['date_of_purchase'], errors='coerce')
    dates_after = df['date_of_purchase'].notna().sum()
    invalid_dates = dates_before - dates_after
    print(f"Invalid date count (became NaT): {invalid_dates}")

    print("\n==================================================")
    print("7. CUSTOMER AGE")
    print("==================================================")
    df['customer_age'] = pd.to_numeric(df['customer_age'], errors='coerce')
    # Flag negative ages as NaN
    invalid_ages = (df['customer_age'] < 0).sum()
    df.loc[df['customer_age'] < 0, 'customer_age'] = np.nan
    print(f"Invalid negative ages treated as missing: {invalid_ages}")

    print("\n==================================================")
    print("8. CSAT")
    print("==================================================")
    df['csat'] = pd.to_numeric(df['csat'], errors='coerce')
    invalid_csat = ((df['csat'] < 1) | (df['csat'] > 5)).sum()
    df.loc[(df['csat'] < 1) | (df['csat'] > 5), 'csat'] = np.nan
    print(f"Invalid CSAT values treated as missing: {invalid_csat}")

    print("\n==================================================")
    print("9. FIRST RESPONSE TIME")
    print("==================================================")
    df['first_response_time'] = pd.to_datetime(df['first_response_time'], errors='coerce')
    frt_valid = df['first_response_time'].notna().sum()
    frt_missing = df['first_response_time'].isna().sum()
    # Invalid count would be the difference between non-null strings before and valid datetimes after
    # But since missing/NaT are mixed, we can just report valid/missing.
    print(f"Valid count: {frt_valid}")
    print(f"Missing/Invalid count: {frt_missing}")
    if frt_valid > 0:
        print(f"Minimum: {df['first_response_time'].min()}")
        print(f"Maximum: {df['first_response_time'].max()}")

    print("\n==================================================")
    print("10. TIME TO RESOLUTION")
    print("==================================================")
    df['time_to_resolution'] = pd.to_datetime(df['time_to_resolution'], errors='coerce')
    ttr_valid = df['time_to_resolution'].notna().sum()
    ttr_missing = df['time_to_resolution'].isna().sum()
    print(f"Valid count: {ttr_valid}")
    print(f"Missing/Invalid count: {ttr_missing}")
    if ttr_valid > 0:
        print(f"Minimum: {df['time_to_resolution'].min()}")
        print(f"Maximum: {df['time_to_resolution'].max()}")

    print("\n==================================================")
    print("11. CATEGORICAL VALIDATION")
    print("==================================================")
    cat_cols = ['ticket_type', 'ticket_status', 'ticket_priority', 'ticket_channel', 'customer_gender']
    for col in cat_cols:
        print(f"\n{col} unique values and counts:")
        print(df[col].value_counts(dropna=False))

    print("\n==================================================")
    print("12. MISSING VALUES")
    print("==================================================")
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    missing_df = pd.DataFrame({'column': missing_counts.index, 'missing_count': missing_counts.values, 'missing_percentage': missing_pct.values})
    missing_df = missing_df.sort_values('missing_percentage', ascending=False)
    missing_df.to_csv(REPORTS_DIR / "cleaning_missing_values.csv", index=False)
    print(missing_df)

    print("\n==================================================")
    print("13. ANALYSIS-READY DERIVED COLUMNS")
    print("==================================================")
    df['purchase_year'] = df['date_of_purchase'].dt.year
    df['purchase_month'] = df['date_of_purchase'].dt.month
    df['purchase_month_name'] = df['date_of_purchase'].dt.strftime('%B')
    
    bins = [0, 17, 25, 35, 45, 55, 65, 120]
    labels = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '66+']
    df['customer_age_group'] = pd.cut(df['customer_age'], bins=bins, labels=labels, right=True)
    
    df['description_length'] = df['ticket_description'].astype(str).str.len()
    
    # resolution_available
    # Yes if resolution contains a non-empty value, No if missing/empty
    def has_resolution(x):
        if pd.isna(x):
            return 'No'
        x_str = str(x).strip()
        if x_str == '' or x_str.lower() == 'nan' or x_str.lower() == 'none':
            return 'No'
        return 'Yes'
    
    df['resolution_available'] = df['resolution'].apply(has_resolution)
    
    # csat_available
    df['csat_available'] = df['csat'].notna().map({True: 'Yes', False: 'No'})
    
    print("Derived columns created.")

    print("\n==================================================")
    print("15. SAVE CLEAN DATASET")
    print("==================================================")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    
    df_reloaded = pd.read_csv(PROCESSED_DATA_PATH)
    final_row_count = len(df_reloaded)
    print(f"Final row count: {final_row_count}")
    print(f"Final column count: {len(df_reloaded.columns)}")
    print(f"Final column names:\n {df_reloaded.columns.tolist()}")
    print(f"Final missing-value summary:\n {df_reloaded.isnull().sum()}")

    print("\n==================================================")
    print("16. CREATE CLEANING REPORT")
    print("==================================================")
    report_lines = [
        f"Original row count: {original_row_count}",
        f"Duplicate rows removed: {duplicate_count_removed}",
        f"Final row count: {final_row_count}",
        f"Invalid dates (became NaT): {invalid_dates}",
        f"Invalid ages (negative): {invalid_ages}",
        f"Invalid CSAT values (outside 1-5): {invalid_csat}",
        f"Missing CSAT percentage: {df['csat'].isna().mean() * 100:.2f}%",
        f"Missing Resolution percentage: {df['resolution'].isna().mean() * 100:.2f}%",
        "Timestamp limitation: Cannot calculate response/resolution duration due to lack of a reliable ticket creation timestamp.",
        "Columns created: purchase_year, purchase_month, purchase_month_name, customer_age_group, description_length, resolution_available, csat_available"
    ]
    
    with open(REPORTS_DIR / "cleaning_report.txt", "w") as f:
        f.write("\n".join(report_lines))
    print("Cleaning report created.")

if __name__ == "__main__":
    main()
