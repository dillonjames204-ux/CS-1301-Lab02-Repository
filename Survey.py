# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Which campus dining spot do you eat at the most?")
    value_input = st.text_input("How would you rate it from 1 to 5?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # 1. Check that the user filled in both boxes.
        if category_input == "" or value_input == "":
            st.warning("Please fill in both questions.")
        # 2. Check that the rating is a whole number from 1 to 5.
        #    (Text inputs always give back strings, so '4' is text, not a number yet.)
        elif not value_input.isdigit() or not (1 <= int(value_input) <= 5):
            st.warning("Please enter a rating that is a whole number from 1 to 5.")
        else:
            # 3. Create a new row of data from 'category_input' and 'value_input'.
            new_row = pd.DataFrame({
                "category": [category_input],
                "value": [value_input],
            })

            # 4. Only write the header row if the file is missing or empty.
            needs_header = not os.path.exists('data.csv') or os.path.getsize('data.csv') == 0

            # 5. Append the new row to 'data.csv'.
            #    mode='a' means 'append', so old rows are kept and the new one goes at the bottom.
            new_row.to_csv('data.csv', mode='a', header=needs_header, index=False)

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")