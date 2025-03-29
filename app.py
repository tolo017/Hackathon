import streamlit as st
from AgriAlert import predict_drought
st.title("AgriAlert Live Demo")
lat = st.number_input("Enter your farm latitude:", value=0.0, format="%.6f")
lon = st.number_input("Enter your farm longitude:", value=0.0, format="%.6f")
if st.button("Predict Drought"):
    alert = predict_drought(lat, lon)
    st.warning(alert)