import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Digital Support Analytics",
    page_icon="📊",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def load_data():
    """
    Load the cleaned dataset from the project root.
    Uses st.cache_data to avoid reloading the 4MB CSV on every user interaction.
    """
    # Assuming script is run from project root: streamlit run app/streamlit_app.py
    data_path = os.path.join("data", "processed", "customer_support_tickets_clean.csv")
    
    if not os.path.exists(data_path):
        st.error(f"Dataset not found at '{data_path}'. Please ensure you are running this app from the project root.")
        return pd.DataFrame()
        
    df = pd.read_csv(data_path)
    
    # Ensure CSAT is strictly numeric to avoid calculation errors
    if 'csat' in df.columns:
        df['csat'] = pd.to_numeric(df['csat'], errors='coerce')
        
    return df

# Load the dataset
df = load_data()

if df.empty:
    st.stop()

# --- Sidebar & Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Dashboard Section:", [
    "1. Support Overview",
    "2. Issue & Ticket Analysis",
    "3. Customer Feedback & Satisfaction",
    "4. Support Channel & Performance"
])

st.sidebar.markdown("---")
st.sidebar.header("Global Filters")
st.sidebar.markdown("Use these filters to drill down across all dashboards.")

# Get unique values for filters (safely dropping NaNs)
all_channels = df['ticket_channel'].dropna().unique().tolist()
all_priorities = df['ticket_priority'].dropna().unique().tolist()
all_types = df['ticket_type'].dropna().unique().tolist()
all_products = df['product_purchased'].dropna().unique().tolist()

# Define filters in sidebar
selected_channels = st.sidebar.multiselect("Select Channel(s)", options=all_channels, default=all_channels)
selected_priorities = st.sidebar.multiselect("Select Priority(s)", options=all_priorities, default=all_priorities)
selected_types = st.sidebar.multiselect("Select Ticket Type(s)", options=all_types, default=all_types)
selected_products = st.sidebar.multiselect("Select Product(s)", options=all_products, default=all_products)

# Filter the dataframe safely based on sidebar selections
filtered_df = df[
    (df['ticket_channel'].isin(selected_channels)) &
    (df['ticket_priority'].isin(selected_priorities)) &
    (df['ticket_type'].isin(selected_types)) &
    (df['product_purchased'].isin(selected_products))
]

# --- Main App Title ---
st.title("Digital Support Analytics & CX Optimization System")
st.markdown("A comprehensive, interactive dashboard providing insights into customer support operations, ticket analysis, and customer feedback.")

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections in the sidebar.")
    st.stop()

# ==========================================
# PAGE 1: SUPPORT OVERVIEW
# ==========================================
if page == "1. Support Overview":
    st.header("1. Support Overview")
    
    # Calculate KPIs
    total_tickets = len(filtered_df)
    open_tickets = len(filtered_df[filtered_df['ticket_status'] == 'Open'])
    closed_tickets = len(filtered_df[filtered_df['ticket_status'] == 'Closed'])
    pending_tickets = len(filtered_df[filtered_df['ticket_status'] == 'Pending Customer Response'])
    avg_csat = filtered_df['csat'].mean()
    
    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Tickets", f"{total_tickets:,}")
    col2.metric("Open Tickets", f"{open_tickets:,}")
    col3.metric("Closed Tickets", f"{closed_tickets:,}")
    col4.metric("Pending Response", f"{pending_tickets:,}")
    col5.metric("Average CSAT", f"{avg_csat:.2f}" if pd.notna(avg_csat) else "N/A")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Ticket Type Distribution (Pie Chart)
        fig_type = px.pie(
            filtered_df, names='ticket_type', 
            title='Ticket Type Distribution', hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig_type, use_container_width=True)
        
        # Priority Distribution (Bar Chart)
        prio_counts = filtered_df['ticket_priority'].value_counts().reset_index()
        prio_counts.columns = ['ticket_priority', 'count']
        fig_priority = px.bar(
            prio_counts, x='ticket_priority', y='count', 
            title='Ticket Priority Distribution',
            labels={'ticket_priority': 'Priority', 'count': 'Tickets'},
            color='ticket_priority', color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_priority, use_container_width=True)
        
    with col_chart2:
        # Channel Distribution (Pie Chart)
        fig_channel = px.pie(
            filtered_df, names='ticket_channel', 
            title='Ticket Channel Distribution', hole=0.4,
            color_discrete_sequence=px.colors.sequential.Mint_r
        )
        st.plotly_chart(fig_channel, use_container_width=True)


# ==========================================
# PAGE 2: ISSUE & TICKET ANALYSIS
# ==========================================
elif page == "2. Issue & Ticket Analysis":
    st.header("2. Issue & Ticket Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Most frequent ticket types
        type_counts = filtered_df['ticket_type'].value_counts().reset_index()
        type_counts.columns = ['ticket_type', 'count']
        fig_freq_type = px.bar(
            type_counts, x='ticket_type', y='count', 
            title="Most Frequent Ticket Types", 
            labels={'ticket_type': 'Ticket Type', 'count': 'Number of Tickets'}
        )
        st.plotly_chart(fig_freq_type, use_container_width=True)
        
        # Products with the most tickets
        prod_counts = filtered_df['product_purchased'].value_counts().reset_index().head(10)
        prod_counts.columns = ['product_purchased', 'count']
        fig_prod = px.bar(
            prod_counts, y='product_purchased', x='count', orientation='h', 
            title="Top Products with Most Tickets",
            labels={'product_purchased': 'Product', 'count': 'Tickets'}
        )
        # Reverse y-axis so the highest count is on top
        fig_prod.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col2:
        # Top ticket subjects
        sub_counts = filtered_df['ticket_subject'].value_counts().reset_index().head(10)
        sub_counts.columns = ['ticket_subject', 'count']
        fig_sub = px.bar(
            sub_counts, y='ticket_subject', x='count', orientation='h', 
            title="Top 10 Ticket Subjects",
            labels={'ticket_subject': 'Subject', 'count': 'Tickets'}
        )
        fig_sub.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_sub, use_container_width=True)
        
        # Ticket status distribution
        fig_status = px.pie(
            filtered_df, names='ticket_status', 
            title="Ticket Status Distribution", hole=0.3
        )
        st.plotly_chart(fig_status, use_container_width=True)


# ==========================================
# PAGE 3: CUSTOMER FEEDBACK & SATISFACTION
# ==========================================
elif page == "3. Customer Feedback & Satisfaction":
    st.header("3. Customer Feedback & Satisfaction")
    
    # Calculate CSAT missing metrics
    total_len = len(filtered_df)
    rated_df = filtered_df[filtered_df['csat'].notna()]
    unrated_df = filtered_df[filtered_df['csat'].isna()]
    
    rated_count = len(rated_df)
    unrated_count = len(unrated_df)
    missing_pct = (unrated_count / total_len * 100) if total_len > 0 else 0
    
    st.warning(f"**Missing Data Notice:** Clearly showing that **{missing_pct:.2f}%** of CSAT values are missing in the currently filtered data. No fake values have been imputed.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Average CSAT", f"{rated_df['csat'].mean():.2f}" if rated_count > 0 else "N/A")
    col2.metric("Rated Tickets", f"{rated_count:,}")
    col3.metric("Unrated Tickets", f"{unrated_count:,}")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Rating distribution
        csat_counts = rated_df['csat'].value_counts().sort_index().reset_index()
        csat_counts.columns = ['CSAT Rating', 'Count']
        # Convert rating to string so plotly treats it as a discrete category
        csat_counts['CSAT Rating'] = csat_counts['CSAT Rating'].astype(str)
        
        fig_dist = px.bar(
            csat_counts, x='CSAT Rating', y='Count', 
            title="CSAT Rating Distribution (1 to 5)",
            labels={'Count': 'Number of Tickets'}
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Rated vs Unrated (Coverage)
        fig_coverage = px.pie(
            names=['Rated', 'Unrated (Missing)'], 
            values=[rated_count, unrated_count], 
            title="CSAT Coverage (Rated vs Unrated)",
            color_discrete_sequence=['#636EFA', '#EF553B']
        )
        st.plotly_chart(fig_coverage, use_container_width=True)
        
    with col_chart2:
        # CSAT by Channel
        csat_channel = rated_df.groupby('ticket_channel')['csat'].mean().reset_index()
        fig_csat_chan = px.bar(
            csat_channel, x='ticket_channel', y='csat', 
            title="Average CSAT by Support Channel",
            labels={'csat': 'Average CSAT', 'ticket_channel': 'Channel'}
        )
        st.plotly_chart(fig_csat_chan, use_container_width=True)
        
        # CSAT by Ticket Type
        csat_type = rated_df.groupby('ticket_type')['csat'].mean().reset_index()
        fig_csat_type = px.bar(
            csat_type, y='ticket_type', x='csat', orientation='h', 
            title="Average CSAT by Ticket Type",
            labels={'csat': 'Average CSAT', 'ticket_type': 'Ticket Type'}
        )
        st.plotly_chart(fig_csat_type, use_container_width=True)

    # CSAT by Product
    st.subheader("Average CSAT by Product")
    csat_prod = rated_df.groupby('product_purchased')['csat'].mean().reset_index().sort_values('csat', ascending=False)
    fig_csat_prod = px.bar(
        csat_prod, x='product_purchased', y='csat', 
        title="Average CSAT by Product",
        labels={'csat': 'Average CSAT', 'product_purchased': 'Product'}
    )
    st.plotly_chart(fig_csat_prod, use_container_width=True)


# ==========================================
# PAGE 4: SUPPORT CHANNEL & PERFORMANCE
# ==========================================
elif page == "4. Support Channel & Performance":
    st.header("4. Support Channel & Performance")
    
    st.info("**Important Data Note:** The supplied timestamps for `first-response-time` and `resolution-time` are independent recorded timestamps rather than a sequential timeline. Therefore, they cannot be reliably used to calculate actual durations (like Time-To-Resolution or Initial Response Time). We analyze their availability instead to understand reporting completeness.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tickets by support channel
        chan_counts = filtered_df['ticket_channel'].value_counts().reset_index()
        chan_counts.columns = ['ticket_channel', 'count']
        fig_chan = px.bar(
            chan_counts, x='ticket_channel', y='count', 
            title="Total Tickets by Support Channel",
            labels={'count': 'Number of Tickets', 'ticket_channel': 'Channel'}
        )
        st.plotly_chart(fig_chan, use_container_width=True)
        
        # Ticket status by channel
        fig_stat_chan = px.histogram(
            filtered_df, x='ticket_channel', color='ticket_status', barmode='group', 
            title="Ticket Status Distribution by Channel",
            labels={'ticket_channel': 'Channel'}
        )
        st.plotly_chart(fig_stat_chan, use_container_width=True)
        
    with col2:
        # Priority by channel
        fig_prio_chan = px.histogram(
            filtered_df, x='ticket_channel', color='ticket_priority', barmode='stack', 
            title="Ticket Priority Make-up by Channel",
            labels={'ticket_channel': 'Channel'}
        )
        st.plotly_chart(fig_prio_chan, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Performance Data Availability (Timestamps)")
    
    col_perf1, col_perf2 = st.columns(2)
    with col_perf1:
        # First-response-time availability
        frt_avail = filtered_df['first_response_time'].notna().value_counts().reset_index()
        frt_avail.columns = ['Available', 'Count']
        frt_avail['Available'] = frt_avail['Available'].replace({True: 'Yes', False: 'No'})
        
        fig_frt = px.pie(
            frt_avail, names='Available', values='Count', 
            title="First Response Time Availability"
        )
        st.plotly_chart(fig_frt, use_container_width=True)
        
    with col_perf2:
        # Resolution availability
        res_avail = filtered_df['resolution_available'].value_counts().reset_index()
        res_avail.columns = ['Available', 'Count']
        
        fig_res = px.pie(
            res_avail, names='Available', values='Count', 
            title="Resolution Value Availability"
        )
        st.plotly_chart(fig_res, use_container_width=True)
