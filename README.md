# Filtered Movie Search

The available API Endpoint makes a call to the OMDb database and returns a filtered list of movies based on their IMDb rating scores

## Installation 

Make an enviroment for the Flask web server inside your desired location

```
python3 -m venv .
```

Activate your environment 

```
source bin/activate
```

Install Flask, Request handling, and Python Dotenv
```
pip install flask python-dotenv requests
```

Set the .env file with the variables
```
OMDB_API_KEY={your key}
OMDB_API_SCHEME=https
OMDB_API_LOC=omdbapi.com
```

## Usage

Set the Flask enviroment variables with

```
export FLASK_APP=index && export FLASK_ENV=development
```

Run the web server with

```
flask run
```

Hit the Endpoint at http::localhost:5000/movie-search/{your search}
```
curl http::localhost:5000/movie-search/furious
```