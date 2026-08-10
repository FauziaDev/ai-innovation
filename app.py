import streamlit as st

st.title("My First AI UI")
st.write("This is a basic UI built with Streamlit")

user_age = st.text_input("What is your age?")
user_message = st.text_input("What is your favorite?")

if st.button("Submit"):
    st.write(user_message)