import pandas as pd
import os

def validate_dataset():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'support_interactions_raw.csv')
    df = pd.read_csv(filepath)
    
    print("Validating Dataset...")
    # Required columns exist
    required_cols = [
        'Ticket_ID', 'Date', 'Customer_ID', 'Channel', 'Customer_Type', 'Product',
        'Issue_Category', 'Sub_Issue', 'Priority', 'Agent_ID', 'First_Response_Min',
        'Resolution_Hours', 'Status', 'Escalated', 'Reopened', 'Contact_Count',
        'SLA_Met', 'CSAT', 'Feedback_Text', 'Sentiment', 'Region'
    ]
    
    missing_cols = set(required_cols) - set(df.columns)
    assert not missing_cols, f"Missing columns: {missing_cols}"
    print("[PASS] All required columns exist.")
    
    # Ticket_ID is unique
    assert df['Ticket_ID'].is_unique, "Ticket_ID is not unique"
    print("[PASS] Ticket_ID is unique.")
    
    # No negative response times
    assert (df['First_Response_Min'] >= 0).all(), "Negative response times found"
    print("[PASS] No negative response times.")
    
    # No negative resolution times
    assert df['Resolution_Hours'].dropna().ge(0).all(), "Negative resolution times found"
    print("[PASS] No negative resolution times.")
    
    # CSAT is between 1 and 5
    assert df['CSAT'].between(1, 5).all(), "CSAT values out of range (1-5)"
    print("[PASS] CSAT values are valid (1-5).")
    
    # Sentiment values are valid
    valid_sentiments = ['Positive', 'Neutral', 'Negative']
    assert df['Sentiment'].isin(valid_sentiments).all(), "Invalid Sentiment values"
    print("[PASS] Sentiment values are valid.")
    
    # Channel values are valid
    valid_channels = ['Live Chat', 'Email', 'Web Form', 'Phone', 'Social Media']
    assert df['Channel'].isin(valid_channels).all(), "Invalid Channel values"
    print("[PASS] Channel values are valid.")
    
    # Priority values are valid
    valid_priorities = ['Low', 'Medium', 'High', 'Critical']
    assert df['Priority'].isin(valid_priorities).all(), "Invalid Priority values"
    print("[PASS] Priority values are valid.")
    
    # Status values are valid
    valid_statuses = ['Resolved', 'Pending', 'Escalated', 'Closed']
    assert df['Status'].isin(valid_statuses).all(), "Invalid Status values"
    print("[PASS] Status values are valid.")
    
    # Required fields do not contain unexpected null values
    non_null_cols = [
        'Ticket_ID', 'Date', 'Customer_ID', 'Channel', 'Customer_Type', 'Product',
        'Issue_Category', 'Sub_Issue', 'Priority', 'Agent_ID', 'First_Response_Min',
        'Status', 'Escalated', 'Reopened', 'Contact_Count',
        'SLA_Met', 'CSAT', 'Feedback_Text', 'Sentiment', 'Region'
    ]
    null_counts = df[non_null_cols].isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    assert cols_with_nulls.empty, f"Unexpected null values in columns: {cols_with_nulls.index.tolist()}"
    print("[PASS] No unexpected null values.")
    
    print("Dataset Validation Passed Successfully!")

if __name__ == "__main__":
    validate_dataset()
