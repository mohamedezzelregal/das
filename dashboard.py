import streamlit as st
import pandas as pd

# Load the data from the CSV files
file_1 = pd.read_csv('1-9-2024.csv')
file_2 = pd.read_csv('2-9-2024.csv')
file_3 = pd.read_csv('3-9-2024.csv')

# Combine the data from the three sessions
data = pd.concat([file_1, file_2, file_3])

# Select the relevant metrics
# Sidebar for filtering options
st.sidebar.header('Filter Options')
selected_players = st.sidebar.multiselect('Select Players', options=data['Player Name'].unique())
selected_date = st.sidebar.selectbox('Select Date', options=data['Date'].unique())

# Filter the data based on selections
filtered_data = data[(data['Player Name'].isin(selected_players)) & (data['Date'] == selected_date)]

# Displaying the filtered data
st.title('Player Performance Dashboard')

st.subheader('Selected Players Performance')
st.write(filtered_data)

# Visualization - Bar chart for the selected players' metrics
st.bar_chart(filtered_data.set_index('Player Name')[['Top Speed (km/h)', 'Dist. Covered (m)']])

# Aggregate metrics for the selected players
st.subheader('Aggregate Performance Over Sessions')
players_data = data[data['Player Name'].isin(selected_players)]
st.write(players_data.groupby(['Player Name', 'Date']).mean()[['Top Speed (km/h)', 'Dist. Covered (m)']])
