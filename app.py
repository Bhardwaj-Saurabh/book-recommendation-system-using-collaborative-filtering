'''
Author: Saurabh Bhardwaj
Email: aryan.saurabhbhardwaj@gmail.com
Date: 19 Jan 2024
'''

import streamlit as st
from src.logger import logging
from src.utils import load_object
from src.pipelines.prediction_pipeline import recommend_book

st.header('Book Recommender System Using ML')

logging.info("Load books title object")
books_title = load_object('artifacts/books_title.pkl')

selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    books_title
)

if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])