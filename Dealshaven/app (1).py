
import streamlit as st
import pandas as pd  # Correct import for pandas
from main import scrape_deals, get_deals
import time

# Streamlit app configuration
st.set_page_config(page_title="Deals Heaven", layout="wide")

# Main content area for store and category selection
st.title("Deals Heaven Scraper")

# Columns for side-by-side dropdowns
col1, col2 = st.columns(2)

with col1:
    # Dropdown for store selection
    stores = ["Flipkart", "Amazon", "Paytm", "Foodpanda", "Freecharge", "Paytmmall"]
    store_name = st.selectbox("Choose a Store", stores)

with col2:
    # Dropdown for category selection
    categories = [
        "All Categories",
        "Beauty And Personal Care",
        "Clothing Fashion & Apparels",
        "Electronics",
        "Grocery",
        "Mobiles & Mobile Accessories",
        "Recharge",
        "Travel Bus & Flight"
    ]
    category_name = st.selectbox("Choose a Category", categories)

# Sidebar for page range input
st.sidebar.header("Page Range")
start_page = st.sidebar.text_input("Start Page", "1")
end_page = st.sidebar.text_input("End Page", "1")

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
            # Trigger the scraping function
            scrape_deals(store_name, category_name, start, end, csv_filename)
            time.sleep(2)  # Optional delay

        st.success("Data scraping and saving completed.")

        # Display data as cards in 6 columns
        data = get_deals(csv_filename)
        st.write("## Scraped Deals")

        # Create 6 columns layout
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        cols = [col1, col2, col3, col4, col5, col6]

        for i, row in data.iterrows():
            with cols[i % 6]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 10px; text-align: center;">
                    <img src="{row['Image']}" alt="Product Image" style="width: 100%; height: auto; border-radius: 5px;">
                    <h4 style="font-size: 14px; font-weight: bold;">{row['Title']}</h4>
                    <p><strong>Price:</strong> {row['Price']}</p>
                    <p><strong>Special Price:</strong> {row['Special Price']}</p>
                    <p><strong>Discount:</strong> {row['Discount']}</p>
                    <p><strong>Rating:</strong> {row['Rating']} ⭐</p>
                    <a href="{row['Link']}" target="_blank" style="color: #fff; background-color: #007BFF; padding: 5px 10px; border-radius: 5px; text-decoration: none;">View Deal</a>
                </div>
                """, unsafe_allow_html=True)

        # Add download button to the sidebar
        with open(csv_filename, "r", encoding="utf-8") as file:
            st.sidebar.download_button(
                label="Download CSV",
                data=file,
                file_name=csv_filename,
                mime="text/csv"
            )

except ValueError:
    st.error("Please enter valid integers for the starting and ending page.")