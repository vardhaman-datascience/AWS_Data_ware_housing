import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS STAGING_EVENTS"
staging_songs_table_drop = "DROP TABLE IF EXISTS STAGING_SONGS"
songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAY"
user_table_drop = "DROP TABLE IF EXISTS USERS"
song_table_drop = "DROP TABLE IF EXISTS SONGS"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS"
time_table_drop = "DROP TABLE IF EXISTS TIME_TABLE"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE STAGING_EVENTS(
artist text , auth text , firstName text , gender text , itemInSession int , lastName text , length text , level text , location text , method text , page text , registration text , sessionId text , song text , status int , ts text , userAgent text , userId text
)
""")

staging_songs_table_create = ("""CREATE TABLE STAGING_SONGS(
artist_id text, artist_latitude text, artist_location text, artist_longitude text, artist_name text, duration text, num_songs int, song_id text, title text, year bigint
)
""")

songplay_table_create = ("""CREATE TABLE SONGPLAY(
songplay_id bigint identity(0, 1), start_time  text, user_id text, level text, song_id text, artist_id text, session_id text, location text, user_agent text
)
""")

user_table_create = ("""CREATE TABLE USERS(
user_id text PRIMARY KEY, first_name text, last_name text, gender text, level text
)
""")

song_table_create = ("""CREATE TABLE SONGS(
song_id text PRIMARY KEY, title text, artist_id text, year bigint, duration text
)
""")

artist_table_create = ("""CREATE TABLE ARTISTS(
artist_id text PRIMARY KEY, name text, location text, lattitude text, longitude text
)
""")

time_table_create = ("""CREATE TABLE TIME_TABLE(
start_time text PRIMARY KEY, hour text, day text, week text, month text, year text, weekday text
)
""")

# STAGING TABLES

staging_events_copy = ("""COPY STAGING_EVENTS
FROM {0}
iam_role {1}
JSON 'auto';
""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'])

staging_songs_copy = ("""COPY STAGING_SONGS
FROM {0}
iam_role {1}
JSON 'auto';
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO SONGPLAY(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT e.ts, e.userId, e.level, s.song_id, s.artist_id, e.sessionId, s.artist_location, e.userAgent
FROM STAGING_EVENTS e
INNER JOIN STAGING_SONGS s 
ON e.artist = s.artist_name
AND e.song = s.title
""")

user_table_insert = ("""INSERT INTO USERS
SELECT DISTINCT userId, firstName,lastName, gender, level
FROM STAGING_EVENTS WHERE userId IS NOT NULL
""")

song_table_insert = ("""INSERT INTO SONGS
SELECT DISTINCT
song_id, title,artist_id, year, duration FROM STAGING_SONGS 
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""INSERT INTO ARTISTS
SELECT DISTINCT artist_id,artist_name, artist_location, artist_latitude, artist_longitude FROM STAGING_SONGS
WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""INSERT INTO time_table (start_time,
hour, day, week, month, year, weekday) SELECT ts, EXTRACT(HOUR FROM ts) AS hour,
EXTRACT (DAY FROM ts) AS day, EXTRACT (WEEK FROM ts) AS week, 
EXTRACT (MONTH FROM ts) AS month, EXTRACT (YEAR FROM ts) AS year,
EXTRACT (DOW FROM ts) AS weekday FROM (SELECT distinct TIMESTAMP 'epoch'
+ ts/1000 *INTERVAL '1second' AS ts FROM STAGING_EVENTS
WHERE ts IS NOT NULL)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
