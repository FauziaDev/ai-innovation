import streamlit as st
st.title("My first AI UI")
st.write("This is a basic UI Built with streamlit")

user_age = st.text("what is your age?")
user_message = st.text_input('what is your favorite')
print(user_message)
if st.button("submit"):
    st.write(user_message)
    