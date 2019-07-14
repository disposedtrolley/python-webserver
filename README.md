# python-webserver

A simple web server implemented in Python.

## Development

### Prerequisites

* Python 3.7
* `pyenv`

### Setup

* Create a new virtual environment in the project directory
    * `pyenv virtualenv env`
* Activate the virtual environment
    * `pyenv activate env`
* Verify that `python` points to the virtual environment
    * `which python`

## Running

* `python server.py` - runs the server, listening on port 8888
* `python client.py` - runs the simple client code, which performs a GET request to localhost:8888
