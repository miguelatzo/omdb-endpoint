# Filtered Movie Search

The available API Endpoint makes a call to the OMDb database and returns a filtered list of movies based on their IMDb rating scores

## Installation 

Make an enviroment for the Flask web server inside your desired location

```
	python3 -m venv .
```

Install Flask and Python Dotenv
```
	pip install flask python-dotenv
```

Set the .env file with the variables
```
	OMDB_API_KEY={your key}
	OMDB_API_SCHEME=https
	OMDB_API_LOC=omdbapi.com
```

## Usage

Run the web server with

```
	flask run
```

Hit the Endpoint at http::localhost:5000/movie-search/{your search}
```
	curl http::localhost:5000/movie-search/furious
```