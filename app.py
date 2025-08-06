import streamlit as st
import numpy as np
import pickle

# Load the trained model
model = pickle.load(open('car_price_prediction.pkl', 'rb'))

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")
st.title("🚗 Car Price Prediction App")
st.write("Enter the details of the car below to predict its estimated selling price.")

# 1. Inputs from user
year = st.number_input("Year of Purchase", min_value=1990, max_value=2025, step=1)
present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, step=0.1)
kms_driven = st.number_input("Kilometers Driven", min_value=0, step=100)
owner = st.selectbox("Owner (0 = First, 1 = Second, 3 = More than two)", [0, 1, 3])
fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG'])
seller_type = st.selectbox("Seller Type", ['Dealer', 'Individual'])
transmission = st.selectbox("Transmission Type", ['Manual', 'Automatic'])

# 2. Manual encoding (one-hot) based on training features

# Fuel Type Encoding
fuel_Petrol = 0
fuel_Diesel = 0
fuel_CNG = 0
if fuel_type == 'Petrol':
    fuel_Petrol = 1
elif fuel_type == 'Diesel':
    fuel_Diesel = 1
elif fuel_type == 'CNG':
    fuel_CNG = 1

# Seller Type Encoding
seller_Dealer = 1 if seller_type == 'Dealer' else 0
seller_Individual = 1 if seller_type == 'Individual' else 0

# Transmission Encoding
transmission_Manual = 1 if transmission == 'Manual' else 0
transmission_Automatic = 1 if transmission == 'Automatic' else 0

# Age of the car
car_age = 2025 - year

# 3. Final input order (must match training data feature order)
input_data = np.array([[present_price, kms_driven, owner, car_age,
                        fuel_CNG, fuel_Diesel, fuel_Petrol,
                        seller_Dealer, seller_Individual,
                        transmission_Manual, transmission_Automatic]])

# 4. Prediction
if st.button("Predict Price"):
    prediction = model.predict(input_data)[0]
    st.success(f" Estimated Selling Price: ₹ {round(prediction, 2)} lakhs")
