# Restaurant schedule API

Web API for converting restaurant schedule into human readable format.
See endpoint tests for input format.

## Requirements
* Internet Access
* Python 3.7 or higher
* Make support

## How to run

* In order to run tests, run ```make test```
* In order to try the API, run ```make run```, open `localhost:8000/docs` in the browser and
  try the `/opening_hours` endpoint
* Run ```make help``` to get help


## My thoughts about the data format

I represent data on the backend side in slightly different format: as a list of objects,
where every object contains corresponding day. I think this format is handier, because
it allows you to sort records by weekday and timestamp values.

Overall, the original data format is okay. It allows you to store week days exactly once.


Another idea, is to store list of objects with Unix timestamps instead of weekdays.
This will allow us to have different schedule for each week, i.e. having the same weekday
multiple times in the input query.


## My assumptions about an input, output and the backend

* Human-readable time is represented in the 12 hours HH:MM format
* Each missing day from input will contain empty list by default, i.e. the restaurant is closed on that day.
* Response will contain data for each day. If day is not supplied in the input, result for this day will be 'Closed'
* Intervals with the same open and close timestamps within one day are ignored
* All records within one day will be sorted by provided timestamp.

## Possible HTTP responses

* HTTP 400 will be returned in the following cases (see tests for more details):
    * There are same consecutive states
    * The last state is 'open'
    * The first state for the first non-empty day is 'close'
* HTTP 422 will be returned in the following cases (see tests for more details):
    * State value neither 'open' nor 'close'
    * Timestamp values are not integers
    * Timestamp values are not in range [0, 86400)
