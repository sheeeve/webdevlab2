# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

file_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
file_path_2 = os.path.join(os.path.dirname(__file__), "..", "organizedData.csv")
jsonFilePath = os.path.join(os.path.dirname(__file__), "..", "data.json")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

try:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(file_path_2)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df) #NEW
except:
    st.warning("The 'organizedData.csv' file is empty or does not exist yet.") 

try:
    with open(jsonFilePath, "r") as f:
        jsonData = json.load(f)

    # Convert to DataFrame
    jsonDataFrame = pd.json_normalize(jsonData)

    st.subheader("Data Preview:")
    st.dataframe(jsonDataFrame)

except:
    st.warning("The 'data.json' file is empty or does not exist yet.")



# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Total Calories per day") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.text("This is a static graph showing the total amount of calories that you have ingested for each day this week.")
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

df_data = current_data_df[['day', 'calories']]
st.bar_chart(df_data.set_index('day'), x_label= "Day of the week", y_label= "Calories",)


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Caloric Intake Data") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.text("This is a dynamic graph showing the average amount of calories a person from each gender in various age ranges eats per day.")
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

g2df = pd.DataFrame(jsonDataFrame)

if "selected_genders" not in st.session_state:
    st.session_state["selected_genders"] = list(g2df["Gender"].unique())

selected_genders = st.multiselect(
    "Select gender(s) to display:",
    options = g2df["Gender"].unique(),
    default = st.session_state["selected_genders"],
    key = "selected_genders"  
)

filtered_df = g2df[g2df["Gender"].isin(st.session_state["selected_genders"])] #NEW

filtered_df = filtered_df.set_index("Gender")
st.bar_chart(filtered_df.T) #NEW



st.title("📈 Calories per Meal by Day")



# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.text("This is a dynamic graph showing the amount of calories you have consumed each day sorted by each meal. You can change the range to change what range of calories is displayed.")
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

#current_data_df
try:
    if "calorie_range" not in st.session_state:
        st.session_state["calorie_range"] = ((current_data_df["calories"].min()), (current_data_df["calories"].max()))


    #NEW
    st.session_state["calorie_range"] = st.slider(
        "Select Calorie Range:",
        min_value=0,
        max_value=(current_data_df["calories"].max()),
        value=st.session_state["calorie_range"],

    )
    low, high = st.session_state["calorie_range"]
    filtered_df = current_data_df[(current_data_df["calories"] >= 0) & (current_data_df["calories"] <= high)]

    pivot_df = filtered_df.pivot_table(index="day", columns="meal", values="calories", aggfunc="sum")

    #NEW
    st.line_chart(pivot_df)
except:
    st.error("Error. Please make sure that you have entered at least one data point into the survey, then refresh your page.")
