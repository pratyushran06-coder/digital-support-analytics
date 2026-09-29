import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# Ensure directories exist
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(RAW_DATA_PATH)

print("==================================================")
print("1. BASIC DATASET PROFILE")
print("==================================================")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print("Column names:\n", df.columns.tolist())
print("\nData types:\n", df.dtypes)
print(f"\nMemory usage:\n{df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
print(f"\nDuplicate row count: {df.duplicated().sum()}")

print("\n==================================================")
print("2. MISSING VALUE ANALYSIS")
print("==================================================")
missing_counts = df.isnull().sum()
missing_pct = (missing_counts / len(df)) * 100
missing_df = pd.DataFrame({'Missing Count': missing_counts, 'Missing Percentage': missing_pct})
missing_df = missing_df.sort_values('Missing Percentage', ascending=False)
print(missing_df)
missing_df.to_csv(REPORTS_DIR / "missing_values_eda.csv")

print("\n==================================================")
print("3. TICKET TYPE ANALYSIS")
print("==================================================")
ticket_types = df['Ticket Type'].value_counts()
ticket_types_pct = df['Ticket Type'].value_counts(normalize=True) * 100
type_analysis = pd.DataFrame({'Count': ticket_types, 'Percentage': ticket_types_pct})
print(type_analysis)
type_analysis.to_csv(REPORTS_DIR / "ticket_type_distribution.csv")

plt.figure(figsize=(10, 6))
ticket_types.plot(kind='bar', color='skyblue')
plt.title('Ticket Type Distribution')
plt.xlabel('Ticket Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "ticket_type_distribution.png")
plt.close()

print("\n==================================================")
print("4. TICKET SUBJECT ANALYSIS")
print("==================================================")
top_subjects = df['Ticket Subject'].value_counts().head(20)
top_subjects_pct = df['Ticket Subject'].value_counts(normalize=True).head(20) * 100
subject_analysis = pd.DataFrame({'Count': top_subjects, 'Percentage': top_subjects_pct})
print(subject_analysis)
subject_analysis.to_csv(REPORTS_DIR / "top_20_ticket_subjects.csv")

plt.figure(figsize=(12, 8))
top_subjects.sort_values().plot(kind='barh', color='coral')
plt.title('Top 20 Ticket Subjects')
plt.xlabel('Count')
plt.ylabel('Subject')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "top_20_ticket_subjects.png")
plt.close()

print("\n==================================================")
print("5. PRODUCT ANALYSIS")
print("==================================================")
products = df['Product Purchased'].value_counts()
products_pct = df['Product Purchased'].value_counts(normalize=True) * 100
product_analysis = pd.DataFrame({'Count': products, 'Percentage': products_pct})
print(product_analysis)
product_analysis.to_csv(REPORTS_DIR / "product_distribution.csv")

plt.figure(figsize=(12, 6))
products.head(20).plot(kind='bar', color='lightgreen')
plt.title('Tickets by Product')
plt.xlabel('Product Purchased')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "tickets_by_product.png")
plt.close()

print("\n==================================================")
print("6. TICKET STATUS ANALYSIS")
print("==================================================")
statuses = df['Ticket Status'].value_counts()
statuses_pct = df['Ticket Status'].value_counts(normalize=True) * 100
status_analysis = pd.DataFrame({'Count': statuses, 'Percentage': statuses_pct})
print(status_analysis)

plt.figure(figsize=(8, 6))
statuses.plot(kind='bar', color='salmon')
plt.title('Ticket Status Distribution')
plt.xlabel('Ticket Status')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "ticket_status_distribution.png")
plt.close()

print("\n==================================================")
print("7. PRIORITY ANALYSIS")
print("==================================================")
priorities = df['Ticket Priority'].value_counts()
priorities_pct = df['Ticket Priority'].value_counts(normalize=True) * 100
priority_analysis = pd.DataFrame({'Count': priorities, 'Percentage': priorities_pct})
print(priority_analysis)

plt.figure(figsize=(8, 6))
priorities.plot(kind='bar', color='orchid')
plt.title('Ticket Priority Distribution')
plt.xlabel('Ticket Priority')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "ticket_priority_distribution.png")
plt.close()

print("\n==================================================")
print("8. CHANNEL ANALYSIS")
print("==================================================")
channels = df['Ticket Channel'].value_counts()
channels_pct = df['Ticket Channel'].value_counts(normalize=True) * 100
channel_analysis = pd.DataFrame({'Count': channels, 'Percentage': channels_pct})
print(channel_analysis)

plt.figure(figsize=(8, 6))
channels.plot(kind='bar', color='gold')
plt.title('Ticket Channel Distribution')
plt.xlabel('Ticket Channel')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "ticket_channel_distribution.png")
plt.close()

print("\n==================================================")
print("9. CHANNEL × TICKET TYPE")
print("==================================================")
channel_type_ct = pd.crosstab(df['Ticket Channel'], df['Ticket Type'])
print(channel_type_ct)

channel_type_ct.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Ticket Channel by Ticket Type')
plt.xlabel('Ticket Channel')
plt.ylabel('Count')
plt.legend(title='Ticket Type')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "channel_vs_ticket_type.png")
plt.close()

print("\n==================================================")
print("10. PRIORITY × STATUS")
print("==================================================")
priority_status_ct = pd.crosstab(df['Ticket Priority'], df['Ticket Status'])
print(priority_status_ct)

plt.figure(figsize=(10, 6))
plt.imshow(priority_status_ct, cmap='YlOrRd')
plt.colorbar(label='Count')
plt.xticks(np.arange(len(priority_status_ct.columns)), priority_status_ct.columns, rotation=45)
plt.yticks(np.arange(len(priority_status_ct.index)), priority_status_ct.index)
for i in range(len(priority_status_ct.index)):
    for j in range(len(priority_status_ct.columns)):
        plt.text(j, i, priority_status_ct.iloc[i, j], ha='center', va='center', color='black')
plt.title('Ticket Priority vs Status')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "priority_vs_status.png")
plt.close()

print("\n==================================================")
print("11. CUSTOMER SATISFACTION")
print("==================================================")
csat = pd.to_numeric(df['Customer Satisfaction Rating'], errors='coerce')
csat_counts = csat.value_counts().sort_index()
csat_pct = csat.value_counts(normalize=True).sort_index() * 100
csat_analysis = pd.DataFrame({'Count': csat_counts, 'Percentage': csat_pct})
print(csat_analysis)

print(f"\nCSAT Mean: {csat.mean():.2f}")
print(f"CSAT Median: {csat.median()}")
print(f"CSAT Std Dev: {csat.std():.2f}")

plt.figure(figsize=(8, 6))
csat_counts.plot(kind='bar', color='teal')
plt.title('Customer Satisfaction Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "customer_satisfaction_distribution.png")
plt.close()

print("\n==================================================")
print("12. SATISFACTION BY CHANNEL")
print("==================================================")
df['CSAT_Numeric'] = pd.to_numeric(df['Customer Satisfaction Rating'], errors='coerce')
csat_by_channel = df.groupby('Ticket Channel')['CSAT_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Number of Rated Tickets', 'mean': 'Average CSAT'})
print(csat_by_channel)

plt.figure(figsize=(10, 6))
csat_by_channel['Average CSAT'].sort_values().plot(kind='bar', color='cyan')
plt.title('Average CSAT by Channel')
plt.xlabel('Ticket Channel')
plt.ylabel('Average CSAT')
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "csat_by_channel.png")
plt.close()

print("\n==================================================")
print("13. SATISFACTION BY TICKET TYPE")
print("==================================================")
csat_by_type = df.groupby('Ticket Type')['CSAT_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Number of Rated Tickets', 'mean': 'Average CSAT'})
print(csat_by_type)

plt.figure(figsize=(10, 6))
csat_by_type['Average CSAT'].sort_values().plot(kind='bar', color='magenta')
plt.title('Average CSAT by Ticket Type')
plt.xlabel('Ticket Type')
plt.ylabel('Average CSAT')
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "csat_by_ticket_type.png")
plt.close()

print("\n==================================================")
print("14. SATISFACTION BY PRIORITY")
print("==================================================")
csat_by_priority = df.groupby('Ticket Priority')['CSAT_Numeric'].agg(['count', 'mean']).rename(columns={'count': 'Number of Rated Tickets', 'mean': 'Average CSAT'})
print(csat_by_priority)

plt.figure(figsize=(10, 6))
csat_by_priority['Average CSAT'].sort_values().plot(kind='bar', color='orange')
plt.title('Average CSAT by Priority')
plt.xlabel('Ticket Priority')
plt.ylabel('Average CSAT')
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig(CHARTS_DIR / "csat_by_priority.png")
plt.close()

print("\n==================================================")
print("15. PRODUCT × TICKET TYPE")
print("==================================================")
product_type_ct = pd.crosstab(df['Product Purchased'], df['Ticket Type'])
print(product_type_ct)
stacked_pt = product_type_ct.stack()
top_combinations = stacked_pt.sort_values(ascending=False).head(5)
print("\nHighest ticket count combinations:")
print(top_combinations)

print("\n==================================================")
print("16. CUSTOMER AGE ANALYSIS")
print("==================================================")
ages = pd.to_numeric(df['Customer Age'], errors='coerce').dropna()
print(f"Minimum Age: {ages.min()}")
print(f"Maximum Age: {ages.max()}")
print(f"Mean Age: {ages.mean():.2f}")
print(f"Median Age: {ages.median()}")
print(f"Std Dev Age: {ages.std():.2f}")

bins = [0, 17, 25, 35, 45, 55, 65, 120]
labels = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '66+']
age_groups = pd.cut(ages, bins=bins, labels=labels, right=True)
age_group_counts = age_groups.value_counts().sort_index()

plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar', color='darkblue')
plt.title('Customer Age Distribution')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "customer_age_distribution.png")
plt.close()

print("\n==================================================")
print("17. PURCHASE DATE ANALYSIS")
print("==================================================")
purchase_dates = pd.to_datetime(df['Date of Purchase'], errors='coerce')
print(f"Earliest purchase date: {purchase_dates.min()}")
print(f"Latest purchase date: {purchase_dates.max()}")
years = purchase_dates.dt.year.value_counts().sort_index()
months = purchase_dates.dt.to_period('M').value_counts().sort_index()

print("\nTickets by purchase year:")
print(years)
print("\nTickets by purchase month:")
print(months)

plt.figure(figsize=(12, 6))
months.plot(kind='line', marker='o', color='green')
plt.title('Tickets by Purchase Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "tickets_by_purchase_month.png")
plt.close()

print("\n==================================================")
print("18. TEXT LENGTH ANALYSIS")
print("==================================================")
desc_lengths = df['Ticket Description'].astype(str).str.len()
print(f"Mean description length: {desc_lengths.mean():.2f}")
print(f"Median description length: {desc_lengths.median()}")
print(f"Minimum description length: {desc_lengths.min()}")
print(f"Maximum description length: {desc_lengths.max()}")

length_by_type = df.groupby('Ticket Type').apply(lambda x: x['Ticket Description'].astype(str).str.len().mean())
print("\nMean Description Length by Ticket Type:")
print(length_by_type)

print("\n==================================================")
print("19. RESOLUTION AVAILABILITY")
print("==================================================")
resolution_missing = df['Resolution'].isnull()
res_counts = resolution_missing.value_counts().rename({True: 'Resolution Missing', False: 'Resolved Information Available'})
print(res_counts)

plt.figure(figsize=(8, 6))
res_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgray'])
plt.title('Resolution Availability')
plt.ylabel('')
plt.tight_layout()
plt.savefig(CHARTS_DIR / "resolution_availability.png")
plt.close()

print("\n==================================================")
print("20. RESPONSE/RESOLUTION TIMESTAMP INSPECTION")
print("==================================================")
first_resp = df['First Response Time']
time_res = df['Time to Resolution']

print("First Response Time data type:", first_resp.dtype)
print("First Response Time missing percentage:", first_resp.isnull().mean() * 100, "%")
try:
    first_resp_dt = pd.to_datetime(first_resp, errors='coerce')
    print("Earliest First Response Time:", first_resp_dt.min())
    print("Latest First Response Time:", first_resp_dt.max())
except:
    print("Could not parse First Response Time as datetime")

print("\nTime to Resolution data type:", time_res.dtype)
print("Time to Resolution missing percentage:", time_res.isnull().mean() * 100, "%")
try:
    time_res_dt = pd.to_datetime(time_res, errors='coerce')
    print("Earliest Time to Resolution:", time_res_dt.min())
    print("Latest Time to Resolution:", time_res_dt.max())
except:
    print("Could not parse Time to Resolution as datetime")

print("\nDuration cannot be reliably calculated from the available timestamps.")

print("\n==================================================")
print("21. KEY FINDINGS")
print("==================================================")

most_freq_ticket_type = ticket_types.index[0] if len(ticket_types) > 0 else "N/A"
top_5_subjects = top_subjects.index[:5].tolist() if len(top_subjects) > 0 else []
top_product = products.index[0] if len(products) > 0 else "N/A"
most_common_channel = channels.index[0] if len(channels) > 0 else "N/A"
most_common_priority = priorities.index[0] if len(priorities) > 0 else "N/A"
most_common_status = statuses.index[0] if len(statuses) > 0 else "N/A"
overall_avg_csat = csat.mean()

top_channel_csat = csat_by_channel.sort_values(by='Average CSAT', ascending=False).iloc[0] if len(csat_by_channel) > 0 else None
top_type_csat = csat_by_type.sort_values(by='Average CSAT', ascending=False).iloc[0] if len(csat_by_type) > 0 else None

pct_missing_resolution = resolution_missing.mean() * 100
pct_missing_csat = csat.isnull().mean() * 100

findings = f"""
1. Most frequent ticket type: {most_freq_ticket_type}
2. Top 5 ticket subjects: {', '.join(top_5_subjects)}
3. Product with the most tickets: {top_product}
4. Most common support channel: {most_common_channel}
5. Most common ticket priority: {most_common_priority}
6. Most common ticket status: {most_common_status}
7. Overall average CSAT: {overall_avg_csat:.2f}
8. Channel with the highest average CSAT: {top_channel_csat.name if top_channel_csat is not None else 'N/A'} (Average: {top_channel_csat['Average CSAT']:.2f}, Sample Size: {top_channel_csat['Number of Rated Tickets']})
9. Ticket type with the highest average CSAT: {top_type_csat.name if top_type_csat is not None else 'N/A'} (Average: {top_type_csat['Average CSAT']:.2f}, Sample Size: {top_type_csat['Number of Rated Tickets']})
10. Percentage of tickets with missing Resolution: {pct_missing_resolution:.2f}%
11. Percentage of tickets with missing CSAT: {pct_missing_csat:.2f}%
12. Important data limitations: Timestamps are provided as independent dates rather than a sequential timeline anchored to a ticket creation date, so durations cannot be reliably calculated. High percentage of missing CSAT ratings.
"""

print(findings)

with open(REPORTS_DIR / "eda_summary.txt", "w") as f:
    f.write(findings.strip())
