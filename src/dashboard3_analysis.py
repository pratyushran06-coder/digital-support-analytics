import pandas as pd
import json
import os

def load_data(file_path):
    """Loads the dataset from the given file path."""
    return pd.read_csv(file_path)

def analyze_csat(df):
    """Performs Customer Feedback & Satisfaction Analysis on the dataset."""
    total_tickets = len(df)
    
    # Ensure csat is numeric
    df['csat'] = pd.to_numeric(df['csat'], errors='coerce')
    
    # Calculate rated and unrated tickets
    rated_mask = df['csat'].notna()
    rated_tickets = int(rated_mask.sum())
    unrated_tickets = int(total_tickets - rated_tickets)
    
    # CSAT Coverage
    csat_coverage = (rated_tickets / total_tickets * 100) if total_tickets > 0 else 0
    
    # Overall Average CSAT
    overall_avg_csat = float(df['csat'].mean()) if rated_tickets > 0 else None
    
    # Average CSAT by dimensions (ignoring NaNs automatically with mean())
    avg_csat_channel = df.groupby('ticket_channel')['csat'].mean().fillna(0).to_dict() if 'ticket_channel' in df.columns else {}
    avg_csat_type = df.groupby('ticket_type')['csat'].mean().fillna(0).to_dict() if 'ticket_type' in df.columns else {}
    avg_csat_product = df.groupby('product_purchased')['csat'].mean().fillna(0).to_dict() if 'product_purchased' in df.columns else {}
    
    # CSAT Rating Distribution
    csat_distribution = df['csat'].value_counts().sort_index().to_dict()
    
    # CSAT Availability Counts
    csat_avail_counts = df['csat_available'].value_counts().to_dict() if 'csat_available' in df.columns else {}
    
    # Missing CSAT
    missing_csat = unrated_tickets
    missing_csat_percentage = (missing_csat / total_tickets * 100) if total_tickets > 0 else 0
    
    # Examples of low CSAT (<= 2)
    low_csat_df = df[df['csat'] <= 2]
    # Select columns that are present in df
    cols_to_include = [c for c in ['ticket_id', 'ticket_channel', 'ticket_type', 'product_purchased', 'ticket_subject', 'ticket_description', 'csat'] if c in df.columns]
    low_csat_examples = low_csat_df[cols_to_include].head(5).to_dict(orient='records')
    
    report = {
        "Total Tickets": total_tickets,
        "Rated Tickets": rated_tickets,
        "Unrated Tickets": unrated_tickets,
        "CSAT Coverage Percentage": csat_coverage,
        "Overall Average CSAT": overall_avg_csat,
        "Average CSAT by Ticket Channel": avg_csat_channel,
        "Average CSAT by Ticket Type": avg_csat_type,
        "Average CSAT by Product": avg_csat_product,
        "CSAT Rating Distribution": csat_distribution,
        "CSAT Availability Counts": csat_avail_counts,
        "Missing CSAT Count": missing_csat,
        "Missing CSAT Percentage": missing_csat_percentage,
        "Low CSAT Examples": low_csat_examples
    }
    
    return report

def main():
    # Construct paths
    data_path = os.path.join("data", "processed", "customer_support_tickets_clean.csv")
    out_dir = os.path.join("outputs", "reports")
    out_path = os.path.join(out_dir, "dashboard3_csat_report.json")
    
    print(f"Loading data from {data_path}...")
    try:
        df = load_data(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {data_path}")
        return

    print("Analyzing Customer Satisfaction...")
    report = analyze_csat(df)
    
    # Print the findings
    print("\n" + "="*60)
    print("=== Dashboard 3: Customer Feedback & Satisfaction Analysis ===")
    print("="*60)
    print(f"Total tickets: {report['Total Tickets']}")
    print(f"Rated tickets: {report['Rated Tickets']}")
    print(f"Unrated tickets (Missing CSAT): {report['Unrated Tickets']} ({report['Missing CSAT Percentage']:.2f}%)")
    print(f"CSAT Coverage: {report['CSAT Coverage Percentage']:.2f}%")
    if report['Overall Average CSAT'] is not None:
        print(f"Overall Average CSAT: {report['Overall Average CSAT']:.2f} / 5.0")
    
    print("\n--- Average CSAT by Channel ---")
    for k, v in report['Average CSAT by Ticket Channel'].items():
        print(f"{k}: {v:.2f}")

    print("\n--- CSAT Rating Distribution ---")
    for k, v in report['CSAT Rating Distribution'].items():
        print(f"Rating {k}: {v} tickets")
        
    print("\n--- CSAT Availability Counts ---")
    for k, v in report['CSAT Availability Counts'].items():
        print(f"{k}: {v} tickets")
        
    print("\n--- Examples of Low CSAT (<= 2) ---")
    if report['Low CSAT Examples']:
        for i, ex in enumerate(report['Low CSAT Examples'], 1):
            ticket_id = ex.get('ticket_id', 'N/A')
            subject = ex.get('ticket_subject', 'N/A')
            rating = ex.get('csat', 'N/A')
            print(f"{i}. Ticket ID {ticket_id}: {subject} (Rating: {rating})")
    else:
        print("No low CSAT examples found.")
        
    print("============================================================\n")
    
    # Save report
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Report successfully saved to {out_path}")

if __name__ == "__main__":
    main()
