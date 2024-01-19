
import numpy as np
from src.utils import load_object
from src.logger import logging

logging.info("Loading trained model")
model = load_object('artifacts/model.pkl')

logging.info("Load books title object")
books_title = load_object('artifacts/books_title.pkl')

logging.info("Loading book matrix")
book_pivot = load_object('artifacts/book_pivot.pkl')

logging.info("Loading ratings")
final_rating = load_object('artifacts/ratings.pkl')


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['url']
        poster_url.append(url)

    return poster_url


def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url   