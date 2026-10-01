
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="SuperKart Sales Forecasting",
    layout="centered"
)

st.title("SuperKart Sales Forecasting")
st.write("Enter product and store details to predict product-store sales.")

# Backend API URL
BACKEND_URL = "https://super-duper-succotash-7vqj44r79vvq395-7860.app.github.dev/predict"

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.0
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.05,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=150.0
)

store_id = st.selectbox(
    "Store ID",
    ["OUT001", "OUT002", "OUT003", "OUT004"]
)

store_establishment_year = st.selectbox(
    "Store Establishment Year",
    [1987, 1998, 1999, 2009]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)

if st.button("Predict Sales"):

    input_data = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Id": store_id,
        "Store_Establishment_Year": store_establishment_year,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type
    }

    try:
        response = requests.post(
            BACKEND_URL,
            json=input_data,
            timeout=30
        )

        if response.status_code == 200:
            prediction = response.json()["predicted_sales"]

            st.success(
                f"Predicted Product-Store Sales: {prediction:,.2f}"
            )

        else:
            st.error(
                f"Prediction failed: {response.text}"
            )

    except Exception as e:
        st.error(
            f"Unable to connect to prediction API: {e}"
        )
