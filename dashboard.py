import streamlit as st
import pandas as pd

# Function to load and concatenate data from multiple files
def load_data(uploaded_files):
    data = pd.DataFrame()
    for file in uploaded_files:
        temp_df = pd.read_csv(file, parse_dates=['Date'])  # Parse date column
        data = pd.concat([data, temp_df], ignore_index=True)
    return data

# File uploader
st.sidebar.header('Upload Datasets')
uploaded_files = st.sidebar.file_uploader("Upload CSV files", accept_multiple_files=True, type="csv")

# Load and combine data if files are uploaded
if uploaded_files:
    data = load_data(uploaded_files)
    
    # Select the relevant metrics
    st.sidebar.header('Filter Options')
    selected_players = st.sidebar.multiselect('Select Players', options=data['Player Name'].unique())

    # Filter the data based on player selection
    players_data = data[data['Player Name'].isin(selected_players)]

    # Displaying the filtered data
    st.title('Player Performance Dashboard')
    st.subheader('Selected Players Performance')
    st.write(players_data)

    if not players_data.empty:
        # Visualization - Bar chart for the selected players' metrics
        st.bar_chart(players_data.groupby('Player Name').mean()[['Top Speed (km/h)', 'Dist. Covered (m)']])

        st.subheader('Aggregate Performance Over Sessions')
        st.write(players_data.groupby(['Player Name', 'Date']).mean()[['Top Speed (km/h)', 'Dist. Covered (m)']])
    
        # Team average calculation
        team_avg = data.groupby('Date').mean()[['Top Speed (km/h)', 'Dist. Covered (m)']].reset_index()
        
        # Check if 'High Intensity Run (m)' column exists
        if 'High Intensity Run (m)' in data.columns:
            team_avg['High Intensity Run (m)'] = data.groupby('Date').mean()['High Intensity Run (m)'].reset_index(drop=True)
        
        # Compare player performance with team average
        st.subheader('Comparison with Team Average')
        comparison_df = players_data.merge(team_avg, on='Date', suffixes=('', '_Team Avg'))
        
        # Display relevant columns based on data availability
        columns_to_display = [
            'Player Name', 'Date', 
            'Top Speed (km/h)', 'Top Speed (km/h)_Team Avg', 
            'Dist. Covered (m)', 'Dist. Covered (m)_Team Avg'
        ]
        
        if 'High Intensity Run (m)' in comparison_df.columns:
            columns_to_display += ['High Intensity Run (m)', 'High Intensity Run (m)_Team Avg']
        
        st.write(comparison_df[columns_to_display])

        # Progress over sessions - Line chart
        st.subheader('Progress Over Sessions')

        # Combine aggregation logic
        metrics = ['Dist. Covered (m)', 'Dist. Covered (m)_Team Avg']
        if 'High Intensity Run (m)' in comparison_df.columns:
            metrics += ['High Intensity Run (m)', 'High Intensity Run (m)_Team Avg']
        
        progress_chart_data = comparison_df.melt(id_vars=['Date', 'Player Name'], 
                                                 value_vars=metrics,
                                                 var_name='Metric', value_name='Value')
        
        # Debugging: Check the structure of progress_chart_data
        st.write("Progress Chart Data:")
        st.write(progress_chart_data.head())
        
        # Simplify the pivot table
        if not progress_chart_data.empty:
            try:
                progress_chart_data_pivot = progress_chart_data.pivot_table(index='Date', columns='Metric', values='Value')
                st.write("Progress Chart Data Pivot:")
                st.write(progress_chart_data_pivot.head())
                
                # Line chart for progress
                st.line_chart(progress_chart_data_pivot)
            except KeyError as e:
                st.error(f"KeyError: {e}. Check the column names in progress_chart_data.")
        else:
            st.write("No data available for progress over sessions.")
        
    else:
        st.write("Please select a player to view the progress.")
else:
    st.write("Please upload CSV files to proceed.")

