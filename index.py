from flask import Flask, jsonify, request
from dotenv import dotenv_values

import logging

import requests

from urllib.parse import urlunsplit, urlencode, quote

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)

@app.route('/movie-search/<hint>', methods=['GET'])
def movie_search(hint):

    hint_safe = quote(hint, safe='')
    query_parameters = urlencode({'s': hint_safe, 'type': 'movie', 'apikey': dotenv_values(".env")["OMDB_API_KEY"]})
    #urlunsplit: scheme, location, path, query, "" 
    url = urlunsplit((dotenv_values(".env")['OMDB_API_SCHEME'], dotenv_values(".env")['OMDB_API_LOC'], "", query_parameters, ""))

    single_hard_coded_search_result = {"Title":"The Fast and the Furious","Year":"2001","Rated":"PG-13","Released":"22 Jun 2001","Runtime":"106 min","Genre":"Action, Crime, Thriller","Director":"Rob Cohen","Writer":"Ken Li, Gary Scott Thompson, Erik Bergquist","Actors":"Vin Diesel, Paul Walker, Michelle Rodriguez","Plot":"Los Angeles police officer Brian O'Conner must decide where his loyalty really lies when he becomes enamored with the street racing world he has been sent undercover to end it.","Language":"English, Spanish","Country":"United States, Germany","Awards":"11 wins & 18 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BZGRiMDE1NTMtMThmZS00YjE4LWI1ODQtNjRkZGZlOTg2MGE1XkEyXkFqcGc@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"6.8/10"},{"Source":"Rotten Tomatoes","Value":"54%"},{"Source":"Metacritic","Value":"58/100"}],"Metascore":"58","imdbRating":"6.8","imdbVotes":"426,570","imdbID":"tt0232500","Type":"movie","DVD":"N/A","BoxOffice":"$144,745,925","Production":"N/A","Website":"N/A","Response":"True"}

    try:
        movie_search = requests.get(url).json()
        logger.info(f"Search: {hint}")
        if "Search" not in movie_search:
            return jsonify({'Search': [], 'error': movie_search['Error']})

        filtered_movie_search = []
        for movie in movie_search['Search']:
            
            query_parameters = urlencode({'i': movie['imdbID'], 'apikey': dotenv_values(".env")["OMDB_API_KEY"]})
            url = urlunsplit((dotenv_values(".env")['OMDB_API_SCHEME'], dotenv_values(".env")['OMDB_API_LOC'], "", query_parameters, ""))
            single_movie_search = requests.get(url).json()
            if "Error" in single_movie_search:
                logger.info(f"Movie: {movie['Title']}, {single_movie_search['Error']}")

            
            logger.info(f"Movie: {single_movie_search['Title']}, imdbRating: {single_movie_search['imdbRating']}")
            if float(single_movie_search['imdbRating']) > 7:
                filtered_movie_search.append({'Title': single_movie_search['Title'],'Year': single_movie_search['Year'],'imdbID': single_movie_search['imdbID'],'Type': single_movie_search['Type'],'Poster': single_movie_search['Poster'],'imdbRating': single_movie_search['imdbRating'],})

    except requests.exceptions.RequestException as ex:
        return jsonify({'Search': [], 'error': ex})

        
    return filtered_movie_search
    