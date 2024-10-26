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
    