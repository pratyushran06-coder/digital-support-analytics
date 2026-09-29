import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_data(num_records=8000):
    np.random.seed(42)
    random.seed(42)
    
    # Definitions
    channels = ['Live Chat', 'Email', 'Web Form', 'Phone', 'Social Media']
    customer_types = ['New', 'Returning']
    products = ['Mobile App', 'Website', 'Payment Service', 'Subscription', 'Online Store', 'Account Service']
    
    issues_map = {
        'Login & Account': ['Forgot Password', 'Account Locked', 'Unable to Login', 'Account Verification'],
        'Payment': ['Payment Failed', 'Payment Pending', 'Duplicate Payment', 'Incorrect Charge'],
        'Technical Problem': ['System Error', 'Feature Not Working', 'Slow Performance', 'Connection Problem'],
        'Refund': ['Refund Delayed', 'Refund Not Received', 'Refund Request', 'Incorrect Refund'],
        'Subscription': ['Cancel Subscription', 'Renewal Problem', 'Subscription Payment', 'Plan Upgrade'],
        'Delivery': ['Late Delivery', 'Missing Delivery', 'Wrong Item', 'Delivery Status'],
        'Website': ['Page Error', 'Website Slow', 'Broken Link', 'Checkout Error'],
        'Mobile App': ['App Crash', 'Login Error', 'Notification Problem', 'App Slow'],
        'Security': ['Suspicious Login', 'Account Security', 'Unauthorized Activity', 'Verification Problem'],
        'General Query': ['Product Information', 'Pricing Question', 'Policy Question', 'General Assistance']
    }
    
    priorities = ['Low', 'Medium', 'High', 'Critical']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    feedback_pos = [
        "Support resolved my issue quickly.",
        "The agent was very helpful.",
        "My problem was solved on the first contact.",
        "Excellent support experience.",
        "Very satisfied with the quick resolution.",
        "Appreciate the fast response and fix."
    ]
    feedback_neu = [
        "The ticket has been created.",
        "I received a response from support.",
        "The issue is being investigated.",
        "Support provided the requested information.",
        "Average experience, got what I needed.",
        "Standard support, nothing special."
    ]
    feedback_neg = [
        "I have been waiting for a response for too long.",
        "My payment failed and the issue is still unresolved.",
        "I had to contact support multiple times.",
        "The problem was not fixed.",
        "Refund is taking too long.",
        "Terrible experience, agents were not helpful.",
        "Very frustrated with the slow resolution."
    ]
    
    data = []
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_records):
        ticket_id = f"TCK-{100000 + i}"
        date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        customer_id = f"CUST-{random.randint(1000, 5000)}"
        agent_id = f"AGT-{random.randint(101, 150)}"
        
        channel = random.choices(channels, weights=[0.3, 0.3, 0.15, 0.2, 0.05])[0]
        customer_type = random.choices(customer_types, weights=[0.3, 0.7])[0]
        product = random.choice(products)
        
        issue_cat = random.choice(list(issues_map.keys()))
        sub_issue = random.choice(issues_map[issue_cat])
        
        priority = random.choices(priorities, weights=[0.3, 0.5, 0.15, 0.05])[0]
        region = random.choice(regions)
        
        # Determine Response and Resolution Time
        if priority == 'Critical':
            resp_min = random.uniform(2, 30)
            res_hours = random.uniform(1, 12)
        elif priority == 'High':
            resp_min = random.uniform(10, 60)
            res_hours = random.uniform(2, 24)
        elif priority == 'Medium':
            resp_min = random.uniform(30, 180)
            res_hours = random.uniform(12, 72)
        else: # Low
            resp_min = random.uniform(60, 360)
            res_hours = random.uniform(24, 120)
            
        # Escalation & related delays
        is_escalated = 'No'
        # Technical, Payment, Refund have higher escalation
        escalation_chance = 0.05
        if issue_cat in ['Technical Problem', 'Payment', 'Refund']:
            escalation_chance = 0.15
        
        if random.random() < escalation_chance:
            is_escalated = 'Yes'
            res_hours *= random.uniform(1.5, 3.0) # Escalation takes longer
            
        # Status
        status_choices = ['Resolved', 'Closed', 'Pending', 'Escalated']
        if is_escalated == 'Yes':
            status = random.choices(status_choices, weights=[0.4, 0.3, 0.1, 0.2])[0]
        else:
            status = random.choices(status_choices, weights=[0.6, 0.3, 0.1, 0.0])[0]
            
        if status == 'Escalated':
            is_escalated = 'Yes'
            
        # Reopened
        reopened = 'Yes' if random.random() < 0.1 else 'No'
        if reopened == 'Yes':
            res_hours *= random.uniform(1.2, 2.0)
            
        contact_count = 1
        if is_escalated == 'Yes':
            contact_count += random.randint(1, 3)
        if reopened == 'Yes':
            contact_count += random.randint(1, 2)
            
        if status == 'Pending':
            res_hours = None
            
        # SLA definition (e.g. Critical < 1h resp, < 8h res)
        sla_met = 'Yes'
        if priority == 'Critical' and (resp_min > 60 or (res_hours and res_hours > 8)):
            sla_met = 'No'
        elif priority == 'High' and (resp_min > 120 or (res_hours and res_hours > 24)):
            sla_met = 'No'
        elif priority == 'Medium' and (resp_min > 240 or (res_hours and res_hours > 72)):
            sla_met = 'No'
        elif priority == 'Low' and (resp_min > 480 or (res_hours and res_hours > 120)):
            sla_met = 'No'
            
        # CSAT
        if status in ['Pending', 'Escalated']:
            base_csat = random.randint(2, 4)
        else:
            base_csat = random.randint(4, 5)
            
        if reopened == 'Yes':
            base_csat -= random.randint(1, 2)
        if contact_count > 2:
            base_csat -= 1
        if sla_met == 'No':
            base_csat -= random.randint(1, 2)
            
        csat = max(1, min(5, base_csat))
        
        # Sentiment
        if csat >= 4:
            sentiment = 'Positive'
        elif csat == 3:
            sentiment = 'Neutral'
        else:
            sentiment = 'Negative'
            
        # Feedback Text
        if sentiment == 'Positive':
            feedback = random.choice(feedback_pos)
        elif sentiment == 'Negative':
            # customize some feedback based on issue
            if 'Refund' in issue_cat:
                feedback = random.choice([f for f in feedback_neg if 'Refund' in f] + feedback_neg)
            elif 'Payment' in issue_cat:
                feedback = random.choice([f for f in feedback_neg if 'payment' in f.lower()] + feedback_neg)
            else:
                feedback = random.choice(feedback_neg)
        else:
            feedback = random.choice(feedback_neu)
            
        # Rounding
        resp_min = round(resp_min, 1)
        if res_hours:
            res_hours = round(res_hours, 1)
            
        data.append([
            ticket_id, date.strftime('%Y-%m-%d %H:%M:%S'), customer_id, channel, customer_type, product,
            issue_cat, sub_issue, priority, agent_id, resp_min, res_hours, status,
            is_escalated, reopened, contact_count, sla_met, csat, feedback, sentiment, region
        ])
        
    cols = [
        'Ticket_ID', 'Date', 'Customer_ID', 'Channel', 'Customer_Type', 'Product',
        'Issue_Category', 'Sub_Issue', 'Priority', 'Agent_ID', 'First_Response_Min',
        'Resolution_Hours', 'Status', 'Escalated', 'Reopened', 'Contact_Count',
        'SLA_Met', 'CSAT', 'Feedback_Text', 'Sentiment', 'Region'
    ]
    
    df = pd.DataFrame(data, columns=cols)
    out_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'support_interactions_raw.csv')
    df.to_csv(out_path, index=False)
    print(f"Dataset generated successfully at {out_path}")
    
    # Display requirements
    print(f"Total number of records: {len(df)}")
    print(f"Total number of columns: {len(df.columns)}")
    print(f"Column names: {', '.join(df.columns)}")
    print("First 5 rows:")
    print(df.head().to_string())
    print("\nMissing-value summary:")
    print(df.isnull().sum().to_string())
    print("\nBasic statistics:")
    print(df.describe(include='all').to_string())

if __name__ == "__main__":
    generate_data()
