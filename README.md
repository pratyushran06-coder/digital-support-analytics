# Digital Support Interaction Analytics System

## Project Purpose
This project analyzes digital customer-support interaction data to identify frequently reported issues, response-time patterns, resolution-time patterns, customer feedback, satisfaction, sentiment, escalations, reopened tickets, SLA performance, and recommendations for improving the online support process.

## Dataset Description
The dataset contains synthetic support interaction records for academic purposes. It includes roughly 8,000 records mimicking realistic customer support interactions.

## Column Descriptions
- `Ticket_ID`: Unique identifier for the support ticket.
- `Date`: Date of the interaction.
- `Customer_ID`: Identifier for the customer.
- `Channel`: Contact channel (Live Chat, Email, Web Form, Phone, Social Media).
- `Customer_Type`: New or Returning.
- `Product`: Product related to the issue.
- `Issue_Category`: Main category of the issue.
- `Sub_Issue`: Specific sub-issue.
- `Priority`: Priority level (Low, Medium, High, Critical).
- `Agent_ID`: Identifier for the support agent.
- `First_Response_Min`: Time to first response in minutes.
- `Resolution_Hours`: Time to resolve the ticket in hours.
- `Status`: Current status of the ticket.
- `Escalated`: Whether the ticket was escalated (Yes/No).
- `Reopened`: Whether the ticket was reopened (Yes/No).
- `Contact_Count`: Number of times the customer contacted support for this ticket.
- `SLA_Met`: Whether the Service Level Agreement was met (Yes/No).
- `CSAT`: Customer Satisfaction score (1 to 5).
- `Feedback_Text`: Customer feedback text.
- `Sentiment`: Sentiment of the feedback (Positive, Neutral, Negative).
- `Region`: Geographic region of the customer.

## How to generate the dataset
Run the generation script:
```bash
python src/generate_dataset.py
```

## How to validate the dataset
Run the validation script:
```bash
python src/validate_dataset.py
```

## How to run tests
Run pytest:
```bash
pytest tests/test_dataset.py
```
