import pandas as pd
import pytest
from pathlib import Path

@pytest.fixture(scope="module")
def raw_df():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    filepath = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
    return pd.read_csv(filepath)

def test_csv_exists():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    filepath = PROJECT_ROOT / "data" / "raw" / "customer_support_tickets.csv"
    assert filepath.exists(), f"File not found at {filepath}"

def test_required_columns(raw_df):
    expected_cols = [
        'Ticket ID', 'Customer Name', 'Customer Email', 'Customer Age',
        'Customer Gender', 'Product Purchased', 'Date of Purchase',
        'Ticket Type', 'Ticket Subject', 'Ticket Description', 'Ticket Status',
        'Resolution', 'Ticket Priority', 'Ticket Channel',
        'First Response Time', 'Time to Resolution', 'Customer Satisfaction Rating'
    ]
    missing = set(expected_cols) - set(raw_df.columns)
    assert not missing, f"Missing columns in raw dataset: {missing}"

def test_ticket_id_exists(raw_df):
    assert 'Ticket ID' in raw_df.columns

def test_min_rows(raw_df):
    assert len(raw_df) > 1000, f"Expected >1000 rows, got {len(raw_df)}"
