# ML-Capstone Project (BizWiz)

This project aims to develop a machine learning model to predict the price of a business listing using natural language processing (NLP). The model is trained on a dataset of business listings, financial data, and industry information.

The project is implemented as a web application with an REST API that can be used by other applications to integrate the price prediction functionality.

## Installation and Usage Instructions

### Build Environment

This project is developed with Mac/Linux, Docker, and Python 3.9.

### Building the Python Package

To build the package, clone the repository and run the following command:

  cd src/; python setup.py sdist;

### Installing the Python Package

To install the package, run the following command:

  cd src/sdist; pip install bizwiz-0.0.1.tar.gz;

### Testing the Python Package

To test the package, run the following command:

  pytest test;      

### Docker Compose

To run the project using Docker Compose use the following command:

  docker-compose up

This will start the Docker containers needed to run the web application and service.
The web application is avaliable at http://localhost:5000 and the REST API is available at http://localhost:5000/api/bizbuysell/url.

### Command line

When the python package is installed, the "bizwiz" cli will be available.

  bizwiz --help

## Features

* Predicts the price of a business listed on BuizBuySell using NLP.
