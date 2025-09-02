# Google Sheets Data Visualization App

This Streamlit app reads data from two publicly accessible Google Sheets and creates visualizations:

1. **Names Data**: Creates a bar chart showing the frequency of each name
2. **Ratings Data**: Creates a line graph showing ratings over time

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Features

- **Bar Chart**: Shows the count of each name from the first Google Sheet
- **Line Graph**: Shows ratings over time from the second Google Sheet
- **Summary Statistics**: Displays key metrics for both datasets
- **Data Refresh**: Button to refresh data from the sheets
- **Responsive Layout**: Side-by-side visualizations

## Data Sources

- **Names Sheet**: [Google Sheet 1](https://docs.google.com/spreadsheets/d/16skHOA6OuX34xDwYv-CsmoAnyqceVyKx1piKN4Wt5T4/edit?usp=sharing)
- **Ratings Sheet**: [Google Sheet 2](https://docs.google.com/spreadsheets/d/1oJoVRfM-4M9K4KRCv_1Te7VzwmWoZkajDf73mal59ZE/edit?usp=sharing)

## Requirements

- Python 3.7+
- Streamlit >= 1.28
- st-gsheets-connection
- pandas
- plotly

## Notes

- The app uses Streamlit's caching to improve performance
- Data is refreshed every 10 minutes by default
- Both Google Sheets must be publicly accessible
- The app handles missing data gracefully with warning messages
