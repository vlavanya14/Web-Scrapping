import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
db_name = "libraries_data.db"

# Initialize session state variables if they don't exist
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "viewing_details" not in st.session_state:
    st.session_state.viewing_details = False

connection = sqlite3.connect(db_name)
state_names = [row[0] for row in connection.execute("SELECT state_name FROM states").fetchall()]

# Step 1: Select a state
if not st.session_state.viewing_details:  # Only show dropdown if not viewing details
    state = st.selectbox("Choose a State", ["Select"] + state_names)
    
    # Step 2: Handle state selection
    if state != "Select":
        st.session_state.selected_state = state  # Update session state
        # Display the Scrape button
        if st.button("Scrape Libraries"):  # When the Scrape button is clicked
            st.session_state.viewing_details = True  # Change to viewing details mode

else:
    # Show libraries details if viewing details
    selected_state = st.session_state.selected_state
    st.title(f"Libraries in {selected_state}")

    query = '''
    SELECT libraries.city, libraries.library, libraries.address, libraries.zip, libraries.phone
    FROM libraries
    JOIN states ON libraries.state_id = states.id
    WHERE states.state_name = ?
    '''
    result = pd.read_sql_query(query, connection, params=(selected_state,))

    # Step 3: Display library details if available
    if result.empty:
        st.write(f"No libraries found for {selected_state}.")
    else:
        st.dataframe(result, use_container_width=True)

    # Add "Back to State Selection" button
    if st.button("Back to State Selection"):
        st.session_state.viewing_details = False  # Reset the flag to go back to dropdown

connection.close()