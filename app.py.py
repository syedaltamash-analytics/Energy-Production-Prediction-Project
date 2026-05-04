#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import joblib
import numpy as np

# Load the saved model
model = joblib.load('/Altamash/Excelr code/PROJECTS/PROJECT_ ENERGY_PRODUCTION/energy_model.pkl')

# Title of the app
st.title('Energy Production Prediction App')

# Instructions
st.write("""
### Predict energy production based on the following inputs:
- Temperature (T)
- Exhaust Vacuum (V)
- Ambient Pressure (AP)
- Relative Humidity (RH)
""")

# Create input fields
temp = st.number_input('Temperature (°C)', min_value=-50.0, max_value=100.0, value=25.0)
vac = st.number_input('Exhaust Vacuum (cm Hg)', min_value=0.0, max_value=100.0, value=50.0)
ap = st.number_input('Ambient Pressure (mbar)', min_value=900.0, max_value=1100.0, value=1013.0)
rh = st.number_input('Relative Humidity (%)', min_value=0.0, max_value=100.0, value=50.0)

# Create a button for prediction
if st.button('Predict'):
    # Create input array for prediction
    input_data = np.array([[temp, vac, ap, rh]])

    # Perform the prediction using the loaded model
    prediction = model.predict(input_data)

    # Display the prediction
    st.success(f'Predicted Energy Production: {prediction[0]:.2f} MW')



# In[ ]:




