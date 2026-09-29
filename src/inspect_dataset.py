import pandas as pd
import os

def inspect_dataset():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'customer_support_tickets.csv')
    if not os.path.exists(filepath):
        print(f"Error: Dataset not found at {filepath}")
        return
        
    df = pd.read_csv(filepath)
    
    print("=== DATASET INSPECTION REPORT ===")
    
    print(f"\n1. Number of rows: {df.shape[0]}")
    print(f"2. Number of columns: {df.shape[1]}")
    print("\n3. Column names:")
    for col in df.columns:
        print(f"  - {col}")
        
    print("\n4. Data types:")
    print(df.dtypes)
    
    print("\n5. First 5 rows:")
    print(df.head())
    
    print("\n6. Last 5 rows:")
    print(df.tail())
    
    print("\n7. Missing-value count:")
    print(df.isnull().sum())
    
    print("\n8. Missing-value percentage:")
    print((df.isnull().sum() / len(df)) * 100)
    
    print("\n9. Number of unique values for each column:")
    print(df.nunique())
    
    print(f"\n10. Duplicate row count: {df.duplicated().sum()}")
    
    # Categorical columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    print("\n=== CATEGORICAL COLUMNS (Top 10 values & frequencies) ===")
    for col in cat_cols:
        print(f"\n- {col}:")
        print(df[col].value_counts(dropna=False).head(10))
        
    # Numeric columns
    num_cols = df.select_dtypes(include=['number']).columns
    if len(num_cols) > 0:
        print("\n=== NUMERIC COLUMNS (Descriptive Statistics) ===")
        print(df[num_cols].describe())
    
    # Specifically inspect requested columns
    print("\n=== SPECIFIC COLUMNS INSPECTION ===")
    cols_to_inspect = ['Ticket Status', 'Ticket Type', 'Ticket Priority', 'Ticket Channel', 'Customer Satisfaction Rating']
    for col in cols_to_inspect:
        if col in df.columns:
            print(f"\n- {col}:")
            print(df[col].value_counts(dropna=False))
        else:
            print(f"\n- {col} (NOT FOUND)")
            
    # Check whether Ticket ID is unique
    if 'Ticket ID' in df.columns:
        is_unique = df['Ticket ID'].is_unique
        print(f"\n=== TICKET ID UNIQUE CHECK ===\nIs 'Ticket ID' unique? {is_unique}")
        if not is_unique:
            print(f"Duplicate 'Ticket ID' count: {df.duplicated(subset=['Ticket ID']).sum()}")
            
    # Check whether time columns are strings or datetime values
    time_cols = ['First Response Time', 'Time to Resolution', 'Date of Purchase']
    print("\n=== TIME COLUMNS TYPE CHECK ===")
    for col in time_cols:
        if col in df.columns:
            first_valid = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
            print(f"- {col}: dtype is {df[col].dtype}, instance type is {type(first_valid)}")
            
            try:
                dt_series = pd.to_datetime(df[col], errors='coerce')
                valid_dt = dt_series.dropna()
                if not valid_dt.empty:
                    print(f"  -> Range for {col}: {valid_dt.min()} to {valid_dt.max()}")
                else:
                    print(f"  -> No valid datetime values parsed for {col}")
            except Exception as e:
                print(f"  -> Could not parse dates for {col}: {e}")
                
    # Detect obvious data-quality problems
    print("\n=== DATA QUALITY OBSERVATIONS ===")
    
    # missing values
    total_missing = df.isnull().sum().sum()
    print(f"- Missing Values: {total_missing} total missing values detected across {len(df.columns[df.isnull().any()])} columns.")
    
    # invalid CSAT values
    if 'Customer Satisfaction Rating' in df.columns:
        csat_numeric = pd.to_numeric(df['Customer Satisfaction Rating'], errors='coerce')
        invalid_csat = csat_numeric[~csat_numeric.between(1, 5) & csat_numeric.notnull()]
        if len(invalid_csat) > 0:
            print(f"- Invalid CSAT values detected (outside 1-5 range): {len(invalid_csat)}")
        else:
            print("- CSAT values appear to be within range (or null).")
            
    # impossible ages
    if 'Customer Age' in df.columns:
        age_numeric = pd.to_numeric(df['Customer Age'], errors='coerce')
        impossible_ages = age_numeric[(age_numeric < 18) | (age_numeric > 100)]
        if len(impossible_ages) > 0:
            print(f"- Potentially impossible ages detected (<18 or >100): {len(impossible_ages)}")
        else:
            print("- Customer ages seem mostly valid based on <18 or >100 thresholds.")

if __name__ == "__main__":
    inspect_dataset()
