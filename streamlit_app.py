import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Google Sheets Data Visualization",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Google Sheets Data Visualization")
st.markdown("This app reads data from two Google Sheets and creates visualizations.")

# Create connection objects for both sheets
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_names_data():
    """Read data from the first Google Sheet (names data)"""
    try:
        conn1 = st.connection("gsheets_names", type=GSheetsConnection)
        df = conn1.read(
            spreadsheet="https://docs.google.com/spreadsheets/d/16skHOA6OuX34xDwYv-CsmoAnyqceVyKx1piKN4Wt5T4/edit?usp=sharing",
            ttl="10m"
        )
        return df
    except Exception as e:
        st.error(f"Error reading names data: {e}")
        return None

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_ratings_data():
    """Read data from the second Google Sheet (ratings data)"""
    try:
        conn2 = st.connection("gsheets_ratings", type=GSheetsConnection)
        df = conn2.read(
            spreadsheet="https://docs.google.com/spreadsheets/d/1oJoVRfM-4M9K4KRCv_1Te7VzwmWoZkajDf73mal59ZE/edit?usp=sharing",
            ttl="10m"
        )
        return df
    except Exception as e:
        st.error(f"Error reading ratings data: {e}")
        return None

# Create two columns for the visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Name Frequency Bar Chart")
    
    # Get names data
    names_df = get_names_data()
    
    if names_df is not None and not names_df.empty:
        st.write("**Raw Data:**")
        st.dataframe(names_df.head())
        
        # Count occurrences of each name
        if 'Name' in names_df.columns:
            name_counts = names_df['Name'].value_counts()
            
            # Create bar chart
            fig_bar = px.bar(
                x=name_counts.index,
                y=name_counts.values,
                title="Frequency of Names",
                labels={'x': 'Name', 'y': 'Count'},
                color=name_counts.values,
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                xaxis_tickangle=-45,
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Display summary statistics
            st.write("**Summary Statistics:**")
            st.write(f"Total names: {len(names_df)}")
            st.write(f"Unique names: {len(name_counts)}")
            st.write(f"Most common name: {name_counts.index[0]} ({name_counts.iloc[0]} times)")
        else:
            st.warning("No 'Name' column found in the data. Please check the sheet structure.")
    else:
        st.warning("No data available from the names sheet.")

with col2:
    st.subheader("📉 Ratings Line Graph")
    
    # Get ratings data
    ratings_df = get_ratings_data()
    
    if ratings_df is not None and not ratings_df.empty:
        st.write("**Raw Data:**")
        st.dataframe(ratings_df.head())
        
        # Create line graph
        if 'Rating' in ratings_df.columns:
            # Add response number column
            ratings_df = ratings_df.reset_index()
            ratings_df['Response_Number'] = ratings_df.index + 1
            
            # Create line chart
            fig_line = px.line(
                ratings_df,
                x='Response_Number',
                y='Rating',
                title="Ratings Over Time",
                labels={'Response_Number': 'Response Number', 'Rating': 'Rating'},
                markers=True
            )
            fig_line.update_layout(
                height=400,
                xaxis_title="Response Number",
                yaxis_title="Rating"
            )
            fig_line.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Display summary statistics
            st.write("**Summary Statistics:**")
            st.write(f"Total responses: {len(ratings_df)}")
            st.write(f"Average rating: {ratings_df['Rating'].mean():.2f}")
            st.write(f"Rating range: {ratings_df['Rating'].min()} - {ratings_df['Rating'].max()}")
        else:
            st.warning("No 'Rating' column found in the data. Please check the sheet structure.")
    else:
        st.warning("No data available from the ratings sheet.")

# Add some additional information
st.markdown("---")
st.markdown("### 📋 Data Sources")
st.markdown("""
- **Names Data**: [Google Sheet 1](https://docs.google.com/spreadsheets/d/16skHOA6OuX34xDwYv-CsmoAnyqceVyKx1piKN4Wt5T4/edit?usp=sharing)
- **Ratings Data**: [Google Sheet 2](https://docs.google.com/spreadsheets/d/1oJoVRfM-4M9K4KRCv_1Te7VzwmWoZkajDf73mal59ZE/edit?usp=sharing)
""")

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
