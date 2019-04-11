# MovieRestApi

Available online at http://milosz.pythonanywhere.com

## /movies/ endpoint

### POST:

* User can add new movie giving __movie_title__ - title will be check for DB 
presence first.
* Based on the title movie details are fetched from OMDb API 
(http://www.omdbapi.com/) - movie title is also check for existence there (
if it is not there, will not be added).
* POST request response include __omdb_details__ fetched from the external API. 

### GET

* User can fetch all movies currently saved to DB.

## /comments/ endpoint

### POST 

* User can add new comment to existing movie giving __movie_id__ and 
__comment_txt__.
* Comments are saved to DB.

### GET

* User can fetch all comments currently saved to DB.
* User can view all comments for certain movie passing __movie_id__ as a 
parameter.

Example
```buildoutcfg
/comments/?movie_id=1
```

## /top/ endpoint

### GET

* Returns top movies present in the DB with ranking based on number of 
comments added to the movie in the specified data range. Response include
ID of the movie, position in rank and total number of comments 
(in the specified date range). 
* Movies with the same number of comments have the same position in the ranking.
* Require specific data range for which statistic is calculated in format 
_dd.mm.yyyy_. In case no data range is selected following default range is
applied _(1.1.2019, today)_.

Example
```buildoutcfg
/top/?date_from=8.4.2019&date_to=9.4.2019
```
Passing above parameters will return all comments in the range 
__[8.4.2019, 9.4.2019)__.

## Third-party libraries

### requests

Used for unit testing POST and GET requests.

### ranking

Used for calculating a dense ranking for top movies.

## Unit tests

Tests for utils functions and all endpoints requests were written using _unittest_
library. Tests invocation from django project main directory:

```buildoutcfg
python tests.py
```
Note: Start app at _0.0.0.0:8000_ before starting tests.

## Hosting

I chose www.pythonanywhere.com instead of www.heroku.com because I already
had experience putting apps at this host. 

