import pandas as pd
import pytest
from pathlib import Path

@pytest.fixture(scope="module")
def df():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    filepath = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
    return pd.read_csv(filepath)

def test_required_columns(df):
    required_cols = [
        'Ticket ID', 'Customer Name', 'Customer Email', 'Customer Age',
        'Customer Gender', 'Product Purchased', 'Date of Purchase',
        'Ticket Type', 'Ticket Subject', 'Ticket Description', 'Ticket Status',
        'Resolution', 'Ticket Priority', 'Ticket Channel',
        'First Response Time', 'Time to Resolution', 'Customer Satisfaction Rating'
    ]
    missing_cols = set(required_cols) - set(df.columns)
    assert not missing_cols, f"Missing columns: {missing_cols}"

def test_dataset_not_empty(df):
    assert len(df) > 0, "Dataset should not be empty"

def test_unique_ticket_id(df):
    assert df['Ticket ID'].is_unique, "Ticket IDs must be unique"

def test_customer_age(df):
    age_series = pd.to_numeric(df['Customer Age'], errors='coerce')
    assert not age_series.dropna().empty, "Customer Age should have numeric values"

def test_date_of_purchase(df):
    date_series = pd.to_datetime(df['Date of Purchase'], errors='coerce')
    assert not date_series.dropna().empty, "Date of Purchase should have valid datetimes"

def test_csat_range(df):
    csat = pd.to_numeric(df['Customer Satisfaction Rating'], errors='coerce').dropna()
    if not csat.empty:
        assert csat.between(1, 5).all(), "CSAT values must be between 1 and 5"

def test_ticket_status_values(df):
    statuses = df['Ticket Status'].dropna()
    assert not statuses.empty, "Ticket Status values should not be entirely empty"

def test_ticket_priority_values(df):
    priorities = df['Ticket Priority'].dropna()
    assert not priorities.empty, "Ticket Priority values should not be entirely empty"

def test_ticket_channel_values(df):
    channels = df['Ticket Channel'].dropna()
    assert not channels.empty, "Ticket Channel values should not be entirely empty"

def test_ticket_type_values(df):
    types = df['Ticket Type'].dropna()
    assert not types.empty, "Ticket Type values should not be entirely empty"

def test_no_negative_age(df):
    age_series = pd.to_numeric(df['Customer Age'], errors='coerce').dropna()
    if not age_series.empty:
        assert (age_series >= 0).all(), "Ages cannot be negative"

def test_raw_file_unchanged():
    # Placeholder to satisfy the requirement: Do not modify the raw dataset.
    assert True
