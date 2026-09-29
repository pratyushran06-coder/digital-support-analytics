import pandas as pd
import numpy as np
import os
import hashlib

def clean_dataset():
    # 1. LOAD DATA
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'customer_support_tickets.csv')
    df = pd.read_csv(raw_path)
    
    orig_rows, orig_cols = df.shape
    
    # 2. REMOVE EXACT DUPLICATE ROWS
    duplicates = df.duplicated()
    dup_count = duplicates.sum()
    df = df[~duplicates].copy()
    
    # duplicate Ticket IDs that are not exact row duplicates
    dup_ticket_ids = df.duplicated(subset=['Ticket ID']).sum() if 'Ticket ID' in df.columns else 0
    
    # 3. STANDARDIZE COLUMN NAMES
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # 4. CLEAN TEXT COLUMNS
    # List all text columns
    text_cols = ['Customer_Name', 'Customer_Email', 'Product_Purchased', 'Ticket_Type', 
                 'Ticket_Subject', 'Ticket_Description', 'Ticket_Status', 'Resolution', 
                 'Ticket_Priority', 'Ticket_Channel', 'Customer_Gender']
    
    for col in text_cols:
        if col in df.columns:
            # strip spaces
            df[col] = df[col].astype(str).str.strip()
            # replace 'nan' and 'None' strings that might have been introduced
            df.loc[df[col].str.lower().isin(['nan', 'none', '']), col] = np.nan

    # 10. STANDARDIZE CATEGORICAL VALUES
    cat_cols_to_std = ['Ticket_Status', 'Ticket_Type', 'Ticket_Priority', 'Ticket_Channel', 'Customer_Gender', 'Product_Purchased']
    
    unique_before = {}
    for col in cat_cols_to_std:
        if col in df.columns:
            unique_before[col] = df[col].dropna().unique()
            df[col] = df[col].astype(str).str.title().str.strip()
            df.loc[df[col].str.lower() == 'nan', col] = np.nan
    
    unique_after = {col: df[col].dropna().unique() for col in cat_cols_to_std if col in df.columns}
    
    # 5. HANDLE CUSTOMER AGE
    df['Customer_Age'] = pd.to_numeric(df['Customer_Age'], errors='coerce')
    invalid_ages = df[(df['Customer_Age'] < 18) | (df['Customer_Age'] > 100)]['Customer_Age'].count()
    df.loc[(df['Customer_Age'] < 18) | (df['Customer_Age'] > 100), 'Customer_Age'] = np.nan
    
    # 6. CLEAN DATE OF PURCHASE
    df['Date_of_Purchase'] = pd.to_datetime(df['Date_of_Purchase'], errors='coerce')
    
    # 7. CLEAN FIRST RESPONSE TIME
    df['First_Response_Time'] = pd.to_datetime(df['First_Response_Time'], errors='coerce')
    
    # 8. CLEAN TIME TO RESOLUTION
    df['Time_to_Resolution'] = pd.to_datetime(df['Time_to_Resolution'], errors='coerce')
    
    # 9. CLEAN CUSTOMER SATISFACTION
    df['Customer_Satisfaction_Rating'] = pd.to_numeric(df['Customer_Satisfaction_Rating'], errors='coerce')
    invalid_csat_mask = ~df['Customer_Satisfaction_Rating'].isin([1, 2, 3, 4, 5]) & df['Customer_Satisfaction_Rating'].notna()
    invalid_csat = df[invalid_csat_mask]['Customer_Satisfaction_Rating'].count()
    df.loc[invalid_csat_mask, 'Customer_Satisfaction_Rating'] = np.nan
    
    # CSAT Category
    conditions = [
        (df['Customer_Satisfaction_Rating'].isin([1, 2])),
        (df['Customer_Satisfaction_Rating'] == 3),
        (df['Customer_Satisfaction_Rating'].isin([4, 5]))
    ]
    choices = ['Dissatisfied', 'Neutral', 'Satisfied']
    df['CSAT_Category'] = np.select(conditions, choices, default=np.nan)
    df.loc[df['CSAT_Category'] == 'nan', 'CSAT_Category'] = np.nan
    
    # 11. CUSTOMER EMAIL / PRIVACY
    def hash_email(email):
        if pd.isna(email):
            return np.nan
        return hashlib.sha256(str(email).encode('utf-8')).hexdigest()[:16]
        
    df['Customer_ID_Anon'] = df['Customer_Email'].apply(hash_email)
    df = df.drop(columns=['Customer_Name', 'Customer_Email'])
    
    # 12. CREATE USEFUL ANALYTICS COLUMNS
    df['Purchase_Year'] = df['Date_of_Purchase'].dt.year
    df['Purchase_Month'] = df['Date_of_Purchase'].dt.month
    df['Purchase_Month_Name'] = df['Date_of_Purchase'].dt.month_name()
    df['Purchase_Day'] = df['Date_of_Purchase'].dt.day
    df['Purchase_Day_Name'] = df['Date_of_Purchase'].dt.day_name()
    
    df['Has_Resolution'] = np.where(df['Resolution'].notna(), 'Yes', 'No')
    df['Has_First_Response'] = np.where(df['First_Response_Time'].notna(), 'Yes', 'No')
    
    # 14. MISSING VALUE REPORT
    missing_report = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
    })
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    missing_report.to_csv(os.path.join(reports_dir, 'missing_value_report.csv'), index=False)
    
    # 15. DATA QUALITY REPORT
    report_lines = [
        "=== DATA QUALITY REPORT ===",
        f"Original Rows: {orig_rows}",
        f"Final Rows: {len(df)}",
        f"Original Columns: {orig_cols}",
        f"Final Columns: {len(df.columns)}",
        f"Exact Duplicates Removed: {dup_count}",
        f"Duplicate Ticket IDs Remaining: {dup_ticket_ids}",
        f"Missing Values (Total): {df.isnull().sum().sum()}",
        f"Invalid Ages Set to NaN: {invalid_ages}",
        f"Invalid/Missing Dates: {df['Date_of_Purchase'].isna().sum()}",
        f"Invalid CSAT Set to NaN: {invalid_csat}",
        "\n--- Unique Categorical Values (Before) ---"
    ]
    
    for col, vals in unique_before.items():
        report_lines.append(f"{col}: {vals}")
        
    report_lines.append("\n--- Unique Categorical Values (After) ---")
    for col, vals in unique_after.items():
        report_lines.append(f"{col}: {vals}")
        
    report_lines.append("\n--- Data Limitations ---")
    report_lines.append("- Missing First Response Time values cannot be computed because there is no ticket creation timestamp.")
    report_lines.append("- Missing Time to Resolution values represent unresolved or pending tickets.")
    
    with open(os.path.join(reports_dir, 'data_quality_report.txt'), 'w') as f:
        f.write('\n'.join(report_lines))
        
    # 16. SAVE CLEAN DATASET
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'customer_support_tickets_clean.csv')
    df.to_csv(out_path, index=False)
    
    # FINAL DISPLAY
    print("1. Final dataset shape:", df.shape)
    print("2. Final column names:", df.columns.tolist())
    print("\n3. Missing-value summary:\n", df.isnull().sum())
    print("\n4. Number of duplicates removed:", dup_count)
    print("\n5. CSAT distribution:\n", df['Customer_Satisfaction_Rating'].value_counts(dropna=False))
    print("\n6. Ticket status distribution:\n", df['Ticket_Status'].value_counts(dropna=False))
    print("\n7. Ticket priority distribution:\n", df['Ticket_Priority'].value_counts(dropna=False))
    print("\n8. Ticket channel distribution:\n", df['Ticket_Channel'].value_counts(dropna=False))
    print("\n9. Ticket type distribution:\n", df['Ticket_Type'].value_counts(dropna=False))
    print("\n10. Raw CSV was NOT modified.")

if __name__ == "__main__":
    clean_dataset()
