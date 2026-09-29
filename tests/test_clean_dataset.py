import pandas as pd
import pytest
from pathlib import Path

@pytest.fixture(scope="module")
def clean_df():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    filepath = PROJECT_ROOT / "data" / "processed" / "customer_support_tickets_clean.csv"
    return pd.read_csv(filepath)

def test_csv_exists():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    filepath = PROJECT_ROOT / "data" / "processed" / "customer_support_tickets_clean.csv"
    assert filepath.exists(), "Clean dataset not found"

def test_required_columns(clean_df):
    expected_cols = [
        'ticket_id', 'customer_name', 'customer_email', 'customer_age',
        'customer_gender', 'product_purchased', 'date_of_purchase',
        'ticket_type', 'ticket_subject', 'ticket_description',
        'ticket_status', 'resolution', 'ticket_priority', 'ticket_channel',
        'first_response_time', 'time_to_resolution', 'csat',
        'purchase_year', 'purchase_month', 'purchase_month_name',
        'customer_age_group', 'description_length', 'resolution_available', 'csat_available'
    ]
    missing_cols = set(expected_cols) - set(clean_df.columns)
    assert not missing_cols, f"Missing columns in clean dataset: {missing_cols}"

def test_no_exact_duplicates(clean_df):
    assert clean_df.duplicated().sum() == 0, "Exact duplicates found in clean dataset"

def test_csat_range(clean_df):
    valid_csat = pd.to_numeric(clean_df['csat'], errors='coerce').dropna()
    assert valid_csat.isin([1.0, 2.0, 3.0, 4.0, 5.0]).all(), "Invalid CSAT values found outside 1-5"

def test_age_validity(clean_df):
    valid_ages = pd.to_numeric(clean_df['customer_age'], errors='coerce').dropna()
    assert (valid_ages >= 0).all(), "Negative ages found"

def test_date_validity(clean_df):
    dates = pd.to_datetime(clean_df['date_of_purchase'], errors='coerce')
    assert not dates.dropna().empty, "No valid dates found"

def test_no_fabricated_metrics(clean_df):
    fabricated = ['response_duration', 'resolution_duration', 'sentiment', 'agent_performance', 'sla_met', 'reopened', 'escalated']
    for col in fabricated:
        assert col not in clean_df.columns, f"Fabricated column found: {col}"
