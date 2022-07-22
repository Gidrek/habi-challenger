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

TODO

## Usage

TODO

## Futures updates



## Problems

* There is not info for `state` so, we can return this info