# tuhabi

## Summary

Habi wants to have a tool where its users can check the properties available for sale. 
In this tool, users must be able to see both the properties sold and those available. 
In order to make the search easier, it is expected that users can apply different filters to the search.

Additionally, it is expected that users can "like" the properties in order to have an internal ranking of the most attractive properties.

## Requirements

We need two microservices

* An endpoint to query properties
* Other to create likes to properties

## Technologies to be used

* Python 3.9

## Development

I going to try develop with pure Python library, not using frameworks and with the queries to the database is going to be
made with raw SQL.

I going to create two main modules:

* server: This is going to be the module to manage the request and the API
* database: this is for create a pseudo ORM to manage the data in the database and queries.

Nice to have:

* Create a Dockerfile and docker-compose.yml file to test
* Deploy to AWS


## Installation

To run the project we need Docker and Docker Compose

First, copy the `.env.example` to a new file called `.env`, and change the required values.

Then run

```
docker compose up -d
```

To run the container

## Usage

You can any HTTP request tool to make GET requests to the endpoing:

### Get all properties

```
curl --location --request GET 'http://localhost:8000/properties/'
```

### Filter by year or city (inclusive)

```
curl --location --request GET 'http://localhost:8000/properties/?year=2000&city=bogota'
```

## Problems

* There is not info for `state` so, we can return this info