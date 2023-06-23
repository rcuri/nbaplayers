# nbaplayers

Python package I created to retrieve player data using the nba-api python package. Uses Celery to create a data pipeline that gets the information and stats for all players that have played in the NBA. After the data retrieval has completed, the final step saves the data into a csv file for each the player profiles and their stats.

I have included the output of running the celery tasks to gather the player's information and the player's career stats in the all_player_profiles.csv and the all_player_stats.csv files, respectively. 

## Celery
For the broker, I used a local instance of a Redis server. If you'd like to change this to use another broker, like RabbitMQ, just switch the `BROKER_URL` in the .env file to the RabbitMQ URL. 

For the backend, I'm running postgres in a local docker container. I'm using the image from Docker Hub for version 14.7 of PostgreSQL. If you'd like to change the backend for Celery to something else, you can change the `RESULT_BACKEND` variable in the .env file to whatever backend you're running on your machine.

## Database
After I retrieve all the data for the players, I store this information in a database so that I can access it from my [api](https://github.com/rcuri/players-api). For local testing, I'm using the same postgres container that I used in the section above, except I'm using a database I created for the API specifically (`basketball` database).

For production, I'm using AWS' RDS to manage my PostgreSQL database. That database is the database that my API is using to retrieve the player data that it returns to users.

I created two tables in my database, a `player` and a `stat` table. To help with searching player's names, I created a column of type tsvector for the player's name directly in a GIN index. Eventually I want to switch this out and replace it with AWS' OpenSearch service, but for now, this will do. 

