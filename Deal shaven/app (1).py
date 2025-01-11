import streamlit as st
import pandas as pd
from main import scrape_deals, get_deals
import time  # For simulating the delay (if needed)

# Streamlit app configuration
st.set_page_config(page_title="Deals Heaven", layout="wide")

# Title below the logo
st.title("Deals Heaven")
# Store selection dropdown in the main body
stores = ["Flipkart", "Amazon", "Paytm", "Foodpanda", "Freecharge", "Paytmmall"]
store_name = st.selectbox("Choose a store", stores)

# Sidebar for page range input
st.sidebar.header("Page Range")
start_page = st.sidebar.text_input("Start Page", "1")
end_page = st.sidebar.text_input("End Page", "1")

sort_option = st.selectbox("Sort By", ["None", "Price", "Discount", "Rating"])

csv_filename = "product_deals.csv"

# Scraping functionality
try:
    start = int(start_page)
    end = int(end_page)

    if start <= 0 or end <= 0:
        st.error("Page numbers must be greater than zero.")
    elif start > end:
        st.error("Starting page must be less than or equal to ending page.")
    elif end > 1703:
        st.error("The DealsHeaven Website has only 1703 Pages!")
    else:
        # Display a spinner while scraping the data
        with st.spinner("Fetching data, please wait..."):
            # Trigger the scraping function from main.py
            scrape_deals(store_name, start, end, csv_filename)
            time.sleep(2)  # Optional delay to simulate longer scraping time (remove in production)

        st.success("Data scraping and saving completed.")

        # Display data as cards in 6 columns
        data = get_deals(csv_filename)
        st.write("## Scraped Deals")

        # Sorting the data based on the selected option
        if sort_option == "Price":
            data = data.sort_values(by='Price', ascending=True)  # Change ascending to False for descending
        elif sort_option == "Discount":
            data = data.sort_values(by='Discount', ascending=False)  # Assuming higher discount is better
        elif sort_option == "Rating":
            data = data.sort_values(by='Rating', ascending=False)  # Assuming higher rating is better

        # Create 6 columns layout
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        cols = [col1, col2, col3, col4, col5, col6]
        
        # Loop through the data and display each product card
        for i, row in data.iterrows():
            with cols[i % 6]:  # Distribute the cards across 6 columns
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 10px; text-align: center;">
                    <img src="{row['Image']}" alt="Product Image" style="width: 100%; height: auto; border-radius: 5px;">
                    <h4 style="font-size: 14px; font-weight: bold;">{row['Title']}</h4>  <!-- Reduced font size for title -->
                    <p><strong>Price:</strong> {row['Price']}</p>
                    <p><strong>Special Price:</strong> {row['Special Price']}</p>
                    <p><strong>Discount:</strong> {row['Discount']}</p>
                    <p><strong>Rating:</strong> {row['Rating']} ⭐</p>
                    <a href="{row['Link']}" target="_blank" style="color: #fff; background-color: #007BFF; padding: 5px 10px; border-radius: 5px; text-decoration: none;">View Deal</a>
                </div>
                """, unsafe_allow_html=True)

        # Download button for CSV in the sidebar
        with open(csv_filename, "r", encoding="utf-8") as file:
            st.sidebar.download_button(
                label="Download CSV",
                data=file,
                file_name=csv_filename,
                mime="text/csv"
            )

except ValueError:
    st.error("Please enter valid integers for the starting and ending page.")