import streamlit as st
import pandas as pd
import subprocess

# Set page title
st.set_page_config(page_title="Behance Job Finder", page_icon="📋")

# Title and description
st.title("Behance Job Finder")


# Input for target company name
st.subheader("Find Specific Job Details")
target_company = st.text_input("Enter the target company name:", placeholder="enter company name")

# Button to find specific job details
if st.button("Find Job Details"):
    if not target_company.strip():
        st.error("Please enter a valid company name.")
    else:
        st.info(f"Searching for job details for '{target_company}'...")
        try:
            result = subprocess.run(
                ["python", "openJobCard.py"],
                input=target_company,
                text=True,
                capture_output=True
            )
            # Display success or error messages
            if result.returncode == 0:
                st.success(f"Successfully searched for '{target_company}'. Check the scraper logs for details.")
            else:
                st.error(f"An error occurred while running the scraper: {result.stderr}")
        except Exception as e:
            st.error(f"Failed to execute the scraper: {e}")

# Separator for UI
st.markdown("---")

# Job Listings Section
st.subheader("Browse Job Listings")
filename = "behance_jobs.csv"
try:
    # Load the CSV file
    data = pd.read_csv(filename)

    # Dropdown menu for company selection
    unique_companies = data['Company'].unique()
    selected_company = st.selectbox("Search for a company", options=["All"] + list(unique_companies))

    # Filter data based on selected company
    if selected_company and selected_company != "All":
        filtered_data = data[data['Company'] == selected_company]
        st.write(f"### Job Listings for '{selected_company}'")
    else:
        filtered_data = data
        st.write("### All Job Listings")

    # Check if there are any job listings to display
    if filtered_data.empty:
        st.warning("No job listings found. Please run the scraper.")
        if st.button("Run Scraper"):
            with st.spinner("Running scraper..."):
                result = subprocess.run(["python", "justScroll.py"], capture_output=True, text=True)
                st.success("Scraping complete! Reload the page to view updated data.")
                st.text(result.stdout)
    else:
        # Create columns for better layout
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        # Display job listings
        for i, (index, row) in enumerate(filtered_data.iterrows()):
            with cols[i % 3]:  # Distribute rows across columns
                st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: #fff;">
                        <img src="{row['image_url']}" alt="Company Logo" style="width: 80px; height: 80px; object-fit: cover; margin-bottom: 10px; transition: transform 0.3s ease;">
                        <h4 style="font-size: 14px; font-weight: bold; color: #333; margin: 10px 0;">{row['Company']}</h4>
                        <p style="color: #666; margin: 5px 0;"><strong>Job Title:</strong> {row['Job Title']}</p>
                        <p style="color: #666; margin: 5px 0;"><strong>Special Description:</strong> {row['Description']}</p>
                        <p style="color: #666; margin: 5px 0;"><strong>Time Posted:</strong> {row['Time Posted']}</p>
                        <p style="color: #666; margin: 5px 0;"><strong>Location:</strong> {row['Location']}</p>
                    </div>
                """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(f"Error: The file `{filename}` was not found. Please ensure the file exists in the same directory as this script.")
    if st.button("Run Scraper"):
        with st.spinner("Running scraper..."):
            result = subprocess.run(["python", "justScroll.py"], capture_output=True, text=True)
            st.success("Scraping complete! Reload the page to view updated data.")
            st.text(result.stdout)
