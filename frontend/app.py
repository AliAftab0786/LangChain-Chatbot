import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from chatbot.rag_chatbot import get_response

# Set up the Streamlit page
st.title("E-commerce Chatbot")
st.write("Ask questions about products, prices, ratings, and more!")

# Input field for user question
query = st.text_input("Enter your question:", placeholder="e.g., What’s the price of Storage Carry Case 27.5cm x 17.5cm x 26cm?")

# Button to submit the question
if st.button("Ask"):
    if query:
        # Get the response from the chatbot
        with st.spinner("Thinking..."):
            response = get_response(query)
        st.write("**Answer:**", response)
    else:
        st.warning("Please enter a question.")

# Sidebar with example questions
st.sidebar.header("Example Questions")
st.sidebar.write("- What’s the price of Storage Carry Case 27.5cm x 17.5cm x 26cm?")
st.sidebar.write("- Which products are under Rs 5,000?")
st.sidebar.write("- What’s the rating of Iced White Single Aperture Mount 12 x 10 Inches?")