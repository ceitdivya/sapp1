import streamlit as st

pg=st.navigation([st.Page("adidas_dash.py",title="Adidash Dashboard"),
st.Page("iris_pred.py",title="Iris species Prediction")
])

pg.run()

