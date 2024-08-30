import streamlit as st
import joblib

st.set_page_config(page_title="Iris species Prediction", page_icon=":evergreen_tree:",layout="wide")

st.title(":ear_of_rice:	Iris species Prediction	:corn:")

model1=joblib.load('svcm1.pkl')

c1,c2=st.columns(2)
n1=c1.number_input("Sepal length")
n2=c2.number_input("Sepal Width")
n3=c1.number_input("Petal Length")
n4=c2.number_input("Petal Width")


new_feature=[[n1,n2,n3,n4]]

if st.button("Model 1 Prediction"):
    t1=model1.predict(new_feature)
    st.subheader("Predicted species is")
    if t1==0:
        st.write("Iris setosa")
        st.image('setosa.jpg')
    elif t1==1:
        st.write("Iris versicolor")
        st.image('versi.jpg')
    elif t1==2:
        st.write("Iris virginica")
        st.image('virginica.jpg')
    else:
        st.write("Flower not listed")