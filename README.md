### Schema for Song Play Analysis
Using the song and event datasets, a star schema has been created and optimized for queries on song play analysis. This includes the following tables.

### Fact Table
songplays - records in event data associated with song plays i.e. records with page NextSong

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
users - users in the app

user_id, first_name, last_name, gender, level

songs - songs in music database

song_id, title, artist_id, year, duration

artists - artists in music database

artist_id, name, location, lattitude, longitude

time - timestamps of records in songplays broken down into specific units

start_time, hour, day, week, month, year, weekday

### Project Template
The project template includes four files:

create_table.py - create fact and dimension tables for the star schema in Redshift.

etl.py is - loads data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

sql_queries.py - defines SQL statements, which will be imported into the two other files above.


### Project Steps
Below are steps you can follow to complete each component of this project.

### Create Table Schemas

Contains SQL CREATE statement for each of these tables in sql_queries.py

Completed the logic in create_tables.py to connect to the database and create these tables

Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, one can run create_tables.py whenever the database needs to be reset and the ETL pipeline needs to be tested.

Launched a redshift cluster and created an IAM role that has read access to S3.

Added redshift database and IAM role info to dwh.cfg.

Tested by running create_tables.py and checking the table schemas in the redshift database. 


### Build ETL Pipeline

Implemented the logic in etl.py to load data from S3 to staging tables on Redshift.

Implemented the logic in etl.py to load data from staging tables to analytics tables on Redshift.

Tested by running etl.py after running create_tables.py and running the analytic queries on the Redshift database to compare the results with the expected results.
