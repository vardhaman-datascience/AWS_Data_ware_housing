### Udacity Data Engineering Project 3 - Data Warehouse in AWS
## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Project Datasets

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
Log data json path: s3://udacity-dend/log_json_path.json
Link: <https://s3.console.aws.amazon.com/s3/buckets/udacity-dend?region=us-west-2&tab=objects>


Tables are denormalised from the JSON Dataset below tables are built.

-- *Fact Table*

    1. songplays - records in event data associated with song plays i.e. records with page NextSong
        songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

-- *Dimension Tables*

    1. users - users in the app
        user_id, first_name, last_name, gender, level
        
    2. songs - songs in music database
        song_id, title, artist_id, year, duration

    3. artists - artists in music database
        artist_id, name, location, lattitude, longitude
    
    4. time - timestamps of records in songplays broken down into specific units
        start_time, hour, day, week, month, year, weekday
<img width="802" alt="Song_ERD" src="https://user-images.githubusercontent.com/56694165/145818252-5733b03d-a786-4074-ad0c-afcc7faf9b72.png">

