# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import string
import pandas as pd
import csv
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

file_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
file_path_2 = os.path.join(os.path.dirname(__file__), "..", "organizedData.csv")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Daily Caloric Tracker 📝")
st.write("Please enter your caloric intake per meal per day for the last week.")


# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form", border=True, clear_on_submit=False):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    dayDict = {}
    mealDict = {}

    day_names = [
        "Monday", 
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]
    meal_names = [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Other",
    ]
    #add index for each day
    for i in range(len(day_names)):
        dayDict[day_names[i]] = i
    #add index for each meal
    for i in range(len(meal_names)):
        mealDict[meal_names[i]] = i

    daySelect = st.selectbox("Please select the day:", day_names)
    mealSelect = st.selectbox("Please select the time of day:", meal_names)

    caloricInput = st.text_input("Enter your caloric intake for this meal:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")
    
    

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if caloricInput == "" or any(c.isalpha() for c in caloricInput):
            st.warning("Please enter an appropriate caloric value!")
        elif float(caloricInput) and int(caloricInput) >= 0:
            if not os.path.exists(file_path):
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["index", "day", "meal", "calories"])

            totalIndex = f"{dayDict[daySelect]}.{mealDict[mealSelect]}"

            with open(file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                existing_entries = [
                    (row["day"], row["meal"]) for row in reader
                ]

            if (daySelect, mealSelect) in existing_entries:
                st.error(f"You already logged {mealSelect} on {daySelect}! Try another meal or day.")
            else:
                with open(file_path, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([totalIndex, daySelect, mealSelect, caloricInput])

                st.success("Your data has been submitted!")
                st.write(f"You ate {caloricInput} calories for {mealSelect} on {daySelect}.")
        else:
            st.warning("Please enter a valid positive number for calories!")

        aInfile = open(file_path, "r")
        dataHeader = aInfile.readline()
        data = sorted(aInfile.readlines())
        aInfile.close()

        dataAll = [dataHeader] + data

        oInfile = open(file_path_2, "w")
        oInfile.writelines(dataAll)
        oInfile.close()
    

reset = st.button("Reset Data")
if reset:
    with open(file_path, "w") as f:
        f.write("index,day,meal,calories\n")
    
    with open(file_path, "r") as f:
        dataHeader = f.readline()
        data = sorted(f.readlines())

    dataAll = [dataHeader] + data

    with open(file_path_2, "w") as f:
        f.writelines(dataAll)

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(file_path_2) and os.path.getsize(file_path_2) > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(file_path_2)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'organizedData.csv' file is empty or does not exist yet.")
