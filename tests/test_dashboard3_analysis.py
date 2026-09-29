import pytest
import pandas as pd
from src.dashboard3_analysis import analyze_csat

@pytest.fixture
def mock_ticket_data():
    """Provides a small, controlled dataset for testing."""
    data = {
        'ticket_id': [1, 2, 3, 4, 5],
        'ticket_type': ['Technical issue', 'Billing inquiry', 'Product setup', 'Technical issue', 'Refund request'],
        'ticket_subject': ['Issue A', 'Issue B', 'Issue C', 'Issue D', 'Issue E'],
        'ticket_description': ['Desc A', 'Desc B', 'Desc C', 'Desc D', 'Desc E'],
        'ticket_channel': ['Email', 'Phone', 'Chat', 'Email', 'Chat'],
        'product_purchased': ['Product X', 'Product Y', 'Product X', 'Product Z', 'Product Y'],
        'csat': [5.0, 1.0, None, 4.0, 2.0],
        'csat_available': ['True', 'True', 'False', 'True', 'True']
    }
    return pd.DataFrame(data)

def test_analyze_csat(mock_ticket_data):
    """Tests that the analyze_csat function calculates metrics correctly."""
    report = analyze_csat(mock_ticket_data)
    
    # 1. Total tickets
    assert report['Total Tickets'] == 5
    
    # 2. Rated tickets
    assert report['Rated Tickets'] == 4
    
    # 3. Unrated tickets
    assert report['Unrated Tickets'] == 1
    
    # 4. CSAT coverage percentage
    assert report['CSAT Coverage Percentage'] == (4 / 5) * 100
    
    # 5. Overall average CSAT
    # Average of 5.0, 1.0, 4.0, 2.0 = 12.0 / 4 = 3.0
    assert report['Overall Average CSAT'] == 3.0
    
    # 6. Average CSAT by ticket channel
    # Email: (5.0 + 4.0) / 2 = 4.5
    # Phone: 1.0
    # Chat: 2.0 (one is None, one is 2.0)
    assert report['Average CSAT by Ticket Channel']['Email'] == 4.5
    assert report['Average CSAT by Ticket Channel']['Phone'] == 1.0
    assert report['Average CSAT by Ticket Channel']['Chat'] == 2.0
    
    # 11. Missing CSAT count and percentage
    assert report['Missing CSAT Count'] == 1
    assert report['Missing CSAT Percentage'] == 20.0
    
    # 12. Examples of low-CSAT interactions (<= 2)
    # Tickets with ID 2 (CSAT 1.0) and 5 (CSAT 2.0)
    low_csat_ids = [ex['ticket_id'] for ex in report['Low CSAT Examples']]
    assert 2 in low_csat_ids
    assert 5 in low_csat_ids
    assert 1 not in low_csat_ids
    assert len(report['Low CSAT Examples']) == 2
