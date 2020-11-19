import configparser



# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events(
    event_id INT IDENTITY(0,1) PRIMARY KEY,
    artist_name VARCHAR(50),
    auth VARCHAR(50),
    first_name VARCHAR(255),
    gender VARCHAR(1),
    item_in_session INTEGER,
    last_name VARCHAR(50),
    song_length FLOAT, 
    level VARCHAR(50),
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration FLOAT,
    session_id BIGINT,
    song_title VARCHAR,
    status INTEGER,
    ts BIGINT,
    user_agent VARCHAR,
    user_id VARCHAR)
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs(
    song_id VARCHAR PRIMARY KEY,
    num_songs INTEGER,
    artist_id VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    location VARCHAR(255),
    name VARCHAR(50),
    title VARCHAR(255),
    duration FLOAT,
    year INTEGER)
""")

songplay_table_create = ("""CREATE TABLE songplays(
    songplay_id INT IDENTITY(1,1) PRIMARY KEY,
    start_time TIMESTAMP REFERENCES time(start_time),
    user_id VARCHAR REFERENCES users(user_id),
    level VARCHAR(50),
    song_id VARCHAR REFERENCES songs(song_id),
    artist_id VARCHAR REFERENCES artists(artist_id),
    session_id BIGINT,
    location VARCHAR(255),
    user_agent TEXT)
""")

user_table_create = ("""CREATE TABLE users(
    user_id VARCHAR PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR(1),
    level VARCHAR(50))
""")

song_table_create = ("""CREATE TABLE songs(
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR NOT NULL,
    year INTEGER,
    duration FLOAT)
""")

artist_table_create = ("""CREATE TABLE artists(
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude FLOAT,
    longitude FLOAT)
""")

time_table_create = ("""CREATE TABLE time(
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER)
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {}
 iam_role {}
 region 'us-west-2'
 JSON {}""").format(config.get('S3','LOG_DATA'),
                        config.get('IAM_ROLE', 'ARN'),
                        config.get('S3','LOG_JSONPATH'))


staging_songs_copy = ("""copy staging_songs from {}
    iam_role {}
    region 'us-west-2'
    JSON 'auto'
    """).format(config.get('S3','SONG_DATA'), 
                config.get('IAM_ROLE', 'ARN'))



# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT 
        TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second' as start_time, 
        se.user_id, 
        se.level,
        ss.song_id,
        ss.artist_id,
        se.session_id,
        se.location,
        se.user_agent
    FROM staging_events se, staging_songs ss
    WHERE se.page = 'NextSong'
    AND se.song_title = ss.title
    AND user_id NOT IN (SELECT DISTINCT s.user_id FROM songplays s WHERE s.user_id = user_id
                       AND s.start_time = start_time AND s.session_id = session_id )
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)  
    SELECT DISTINCT 
        user_id,
        first_name,
        last_name,
        gender, 
        level
    FROM staging_events
    WHERE page = 'NextSong'
    AND user_id NOT IN (SELECT DISTINCT user_id FROM users)
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
    SELECT DISTINCT 
        song_id, 
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs)
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    SELECT DISTINCT 
        artist_id,
        name,
        location,
        latitude,
        longitude
    FROM staging_songs
    WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists)
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT 
        start_time, 
        EXTRACT(hr from start_time) AS hour,
        EXTRACT(d from start_time) AS day,
        EXTRACT(w from start_time) AS week,
        EXTRACT(mon from start_time) AS month,
        EXTRACT(yr from start_time) AS year, 
        EXTRACT(weekday from start_time) AS weekday 
    FROM (
        SELECT DISTINCT  TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second' as start_time 
        FROM staging_events se     
    )
    WHERE start_time NOT IN (SELECT DISTINCT start_time FROM time)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
