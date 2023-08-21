# Title: Youtube Data Harvesting and Warehousing Using MongoDb, SQL, Streamlit
## Problem Statement
Problem Statement:
The problem statement is to create a Streamlit application that allows users to access
and analyze data from multiple YouTube channels. The application should have the
following features:
1. Ability to input a YouTube channel ID and retrieve all the relevant data
(Channel name, subscribers, total video count, playlist ID, video ID, likes,
dislikes, comments of each video) using Google API.
2. Option to store the data in a MongoDB database as a data lake.
3. Ability to collect data for up to 10 different YouTube channels and store them in
the data lake by clicking a button.
4. Option to select a channel name and migrate its data from the data lake to a
SQL database as tables.
5. Ability to search and retrieve data from the SQL database using different
search options, including joining tables to get channel details.

## Technologies used
1. Python
2. Mysql
3. MongoDB
4. Stremlit

## Approach
1. Start by setting up a streamlit application, which provides interface for users to enter channel_id as input and can get the channel details.
2. Establish a connection to the YouTube API V3, which allows to retrieve channel and video data by utilizing the Google API client library for Python.4.
3. Writing functions to retrive the data of channel_details, video_details and comment_details.
4. Store the retrived data in MongoDB, as it is a suitable choice for handling unstructured data. These are stored in 3 different collections channels,videos and columns.
5. Trasforming the data to SQl using SQL database mysql.
6. Utilizing mysql queries to get the answers for required questions.
7. The answers for the mentioned questions are displayed through the streamlit application.
