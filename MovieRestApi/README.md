# MovieRestApi

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