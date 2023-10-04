# Project Description

The project provides Rest API service implementation written in Python by using Django REST Framework.
The purpose of the service creation is to provide interface for sentiment analysis of the text. The service get some 
text or batch of texts on input and returns tonality tags along with score values as a result.

# Sentiment analysis

Sentiment analysis implementation is basing on "asent" model from spaCy.

We use spacy pipeline for sentiment analysis. The `analyze` function takes text to be analyzed, integrates the "asent"
model from spaCy library, creates pipeline objects during initialisation and returns dictionary with analyzed results:
* `negative` - negative score of the passed text
* `neutral` - neutral score of the passed text
* `positive` - positive score of the passed text
* `compound` - compound value of the scores for passed text

# Project's code structure

The project is based on Django Rest Framework and contains following applications:

## ciphixanalyzer

This is the main module of the project. It contains code for the internal needs of the Django REST Framework,
settings file for the project and the urls configuration file.

## analyzer

The application provides the implementation of Rest API functions. The application contains one model AnalysisResults
to store analysis calls log for each user. There are also implementation of the Rest API endpoints in view and
serializer classes:
* AnalysisSerializer - serialize analysis results
* InputSerializer - serialize text to be passed for analysis
* CallLog - implementation of `logs` endpoint
* Analyze - implementation of `analyze` endpoint
* AnalyzeBatch - implementation of `analyze_batch` endpoint

## Docker

The project also contains Dockerfile in the root of the project's directory. The file is using to build Docker image
which contains Ciphix Analyzer Rest API implementation. 

### How to build Docker image

In the root project directory run the following command:
```shell
sudo docker build --tag ciphix-rest-api .
```

### How to run service in Docker image

As you have Docker image built, say with name `ciphix-rest-api`, you can run service by using this image either for
test purposes:
```shell
sudo docker run --rm -it --network=host ciphix-rest-api
```

or as daemon to provide service in 24X7 mode:
```shell
sudo docker run --name=CONTAINER_NAME -d --restart=always -p 8000:EXTERNAL_PORT_NUMBER ciphix-rest-api
```

# Microsoft Azure virtual machine

The service is acceptable in Microsoft Azure host machine by IP address 20.47.114.156 and port number 8000.
The service works on the target machine in Docker image. One admin user is registered with name `larisa` and 
two ordinary users: 
* `mefrill`
* `milky`

# Rest API endpoints

There are following endpoints implemented by the service:
* `admin/` - endpoint for access to the Django REST Framework administration functionality
* `api-auth/` - endpoint for the API service users authentication 
* `analyze/` - endpoint that accepts requests with text data to be analyzed, validating data, analyze it and saves 
analysis results to the database
* `logs/` - endpoint to view historic calls for the authenticated user
* `accounts/profile/` - displays historic calls for the authenticated user
* `analyze_batch/` - endpoint that accepts requests with collection of text data, validating it, analyze and saves 
analysis results to the database all at once.

# Scalability and Performance

Currently, the project is implemented as a prototype. That means that architecture of the project does not provide
possibility to extend in time by taking in account traffic increase. We need to redesign the project architecture 
to make the service scalable. 

The service keeps analyze calls log in the database. The other part of the project is stateless. We need to separate
stateful part of the service from stateless one. To do that we need to:
1. Move database implementation to separate cluster (maybe use scalable DB implementation like Cassandra). 
2. Implement lightweight DRF based part of the project in many separate containers.
3. Use some router service (for example Nginx) to pass user requests to lightweight parts.