# Importing required Libraries
from googleapiclient.discovery import build
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd

import pymongo
from pymongo import MongoClient

import mysql.connector as sql

# Setting Configurations
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing",
                   page_icon=":rocket:",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': "# Kishorekumar Nadipena"})

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Youtube_details"]

mydb = sql.connect(host="localhost",
                   user="root",
                   password="Kishore@95",
                   database="youtube_details"
                   )
mycursor = mydb.cursor()

# api_key = "AIzaSyAeL9OerXl8e8OApXpiwVPJpEStrHerpuQ"
# api_key = "AIzaSyCQMqRdxT8OMTB4sPZwwV_SSS4JLyTB7KU"
api_key = "AIzaSyDX6FksyynMsCDwfo_FochwIanGaoAtO5s"

api_service_name = "youtube"
api_version = "v3"
youtube = build(
    api_service_name, api_version, developerKey=api_key)

# Functions to extract data using youtube api
def get_channel_details(channel_id):
    channel_details = list()
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    for item in response['items']:
        details = {'Channel_Id': channel_id,
                   'Channel_Name': item['snippet']['title'],
                   'Subscribers': item['statistics']['subscriberCount'],
                   'Channel_Views': item['statistics']['viewCount'],
                   'Total_Videos': item['statistics']['videoCount'],
                   'Channel_Description': item['snippet']['description'],
                   'Playlist_Id': item['contentDetails']['relatedPlaylists']['uploads']
                   }
        channel_details.append(details)

    return channel_details


def get_video_ids(channel_id):
    video_ids = list()
    request = youtube.channels().list(
        part="snippet,contentDetails",
        id=channel_id
    )
    response = request.execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    return video_ids


def get_video_details(video_ids):
    all_videos_info = list()

    for i in range(len(video_ids)):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ids[i]
        )

        response = request.execute()

        for video in response['items']:
            video_details = {'Channel_Name': video['snippet']['channelTitle'],
                             'Video_Id': video['id'],
                             'Channel_Id': video['snippet']['channelId'],
                             'Title': video['snippet']['title'],
                             'Tags': str(video['snippet'].get('tags')),
                             'Thumbnail': video['snippet']['thumbnails']['default']['url'],
                             'Description': video['snippet']['description'],
                             'Published_Date': video['snippet']['publishedAt'],
                             'Duration': video['contentDetails']['duration'],
                             'Views': video['statistics']['viewCount'],
                             'Likes': video['statistics'].get('likeCount'),
                             'Comments': video['statistics'].get('commentCount'),
                             'Favorite_Count': video['statistics']['favoriteCount'],
                             'Definition': video['contentDetails']['definition'],
                             'Caption_Status': video['contentDetails']['caption']
                             }
            all_videos_info.append(video_details)

    return all_videos_info


def get_comments_details(video_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            request = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=video_id,
                                                    maxResults=100,
                                                    pageToken=next_page_token)
            response = request.execute()
            for comment in response['items']:
                data = {'Comment_Id': comment['id'],
                        'Video_Id': comment['snippet']['videoId'],
                        'Comment_Text': comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'Comment_Author': comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'Comment_Published_At': comment['snippet']['topLevelComment']['snippet']['publishedAt']
                        }
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break

    except:
        pass
    return comment_data


def all_comments(video_ids):
    comments = list()
    for video_id in video_ids:
        comments += get_comments_details(video_id)
    return comments


def channel_names():
    channels = list()
    for i in db.channels.find():
        channels.append(i['Channel_Name'])
    return channels


def channel_ids():
    ids = list()
    for i in db.channels.find():
        ids.append(i['Channel_Id'])
    return ids

# Functions to load data to Sql
def insert_into_channels():
    query = "INSERT INTO channels VALUES (%s,%s,%s,%s,%s,%s,%s)"
    for doc in db.channels.find({'Channel_Name': ch_input}, {'_id': 0}):
        values = tuple(doc.values())
        mycursor.execute(query,values)
        mydb.commit()
def insert_into_videos():
    query = "INSERT INTO videos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for doc in db.videos.find({'Channel_Name': ch_input}, {'_id': 0}):
        values = tuple(doc.values())
        mycursor.execute(query, values)
        mydb.commit()

def insert_into_comments():
    query = "INSERT INTO comments VALUES (%s,%s,%s,%s,%s)"
    for vid in db.videos.find({'Channel_Name': ch_input}, {'_id': 0}):
        for i in db.comments.find({'Video_Id':vid['Video_Id']},{'_id':0}):
            values = tuple(i.values())
            mycursor.execute(query, values)
            mydb.commit()

# Streamlit code
with st.sidebar:
    options = option_menu('Menu',options=['Home','Work','About'],icons = ['house','gear','person-vcard-fill'])

if options == 'Home':
    st.title(':house: Home')
    st.write('### :red[Project Name]: Youtube Data Harvesting and Warehousing')
    st.write('### :red[Technologies Used]: MongoDB, SQL, Streamlit')
    st.write('### :red[Skills Required]: Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB and SQL')
    st.write('### :red[Domain]: Social Media')
    st.write('''### :red[Overview]: This project encompasses a comprehensive YouTube data system. Utilizing the YouTube Data API, it collects and structures video details, comments, and user profiles. Data is seamlessly managed across MongoDB and SQL databases, ensuring efficiency for both structured and unstructured information. The system's highlight is the Streamlit-powered dashboard, offering an intuitive interface. ''')
    #  to visualize trends and insights within the YouTube dataset
    image = Image.open("C:/Users/kisho/Downloads/flow.png")
    st.image(image)

elif options == 'Work':
    st.title(':hourglass: Working with the data')
    tab1,tab2,tab3 = st.tabs([':information_source: Instructions',':arrow_down: Import & :arrow_up: export',':eye: view'])
    with tab1:
        st.subheader('Steps to follow :feet:')
        st.write(":red[Step-1] : Go to :arrow_down: Import & :arrow_up: export, enter channel id you like ")
        st.info('''Steps to get channel_id                 
                       1. Open home page of a YouTube channel you like                 
                       2. Click ctrl+u to open source page                 
                       3. Select line wrap on above left                 
                       4. Click ctrl+f and search for "?channel"''')
        st.write(":red[Step-2] : Click on Get button to get the channel details ")
        st.write(":red[Step-3] : Click on Upload to MongoDB button to upload channel details to MongoDB")
        st.write(":red[Step-4] : Select a channel name from dropdown to transform data to MySql")
        st.write(":red[Step-5] : Click on Transform button to Transform the MongoDB data to MySql")
        st.write(":red[step-6] : Go to :eye: view, select the question you want.")
    with tab2:
        id_input = st.text_input('Channel_id')
        get_button = st.button('Get')

        if id_input and get_button:
            if id_input not in channel_ids():
                with st.spinner(":green[Getting the channel details]"):
                    c_details = get_channel_details(id_input)
                    st.success(f"Collected thLe details of {c_details[0]['Channel_Name']} Succesfully", icon="✅")
                    st.table(c_details)
            else:
                st.info('Channel details are already available', icon="ℹ️")


        if st.button("Upload to MongoDB"):
            with st.spinner("Uploading Channel Details"):
                c_details = get_channel_details(id_input)
                st.toast('got the channel details Successfully', icon='😍')
                v_ids = get_video_ids(id_input)
                st.toast('got the video ids Successfully', icon='😍')
                v_details = get_video_details(v_ids)
                st.toast('got the video details Successfully', icon='😍')
                cmt_details = all_comments(v_ids)
                st.toast('got the comment details Successfully', icon='😍')

                db.channels.insert_many(c_details)
                db.videos.insert_many(v_details)
                try:
                    db.comments.insert_many(cmt_details)
                except:
                    st.warning('No comments for this channel')
                st.success(f"Uploaded the details of {c_details[0]['Channel_Name']} Succesfully", icon="✅")

        channels = channel_names()
        channels.insert(0, 'Choose a channel')
        ch_input = st.selectbox("Available channels are below", options=channels)
        transform = st.button('Transform to Sql')

        if ch_input and transform:
            try:
                with st.spinner("Transforming MongoDB data to Sql"):
                    insert_into_channels()
                    insert_into_videos()
                    insert_into_comments()
                    st.success('Successfully transformed!', icon="✅")
            except:
                st.error("channel details already transformed", icon="🚨")

    with tab3:
        questions = ['Select a question',
                     '1. What are the names of all the videos and their corresponding channels?',
                     '2. Which channels have the most number of videos, and how many videos do they have?',
                     '3. What are the top 10 most viewed videos and their respective channels?',
                     '4. How many comments were made on each video, and what are their corresponding video names?',
                     '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                     '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                     '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                     '8. What are the names of all the channels that have published videos in the year 2022?',
                     '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                     '10. Which videos have the highest number of comments, and what are their corresponding channel names?']

        question = st.selectbox('Select the query', options=questions)

        if question == '1. What are the names of all the videos and their corresponding channels?':
            query = 'SELECT Title, Channel_name from videos;'
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('videos and their channel name')
            st.write(df)

        elif question == '2. Which channels have the most number of videos, and how many videos do they have?':
            query = '''Select channel_name, Count(video_id) total_videos
                       from videos 
                       group by channel_name 
                       order by total_videos DESC;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Channels with most videos')
            st.write(df)

        elif question == '3. What are the top 10 most viewed videos and their respective channels?':
            query = '''SELECT title, views, channel_name
                       FROM videos
                       ORDER BY views DESC
                       LIMIT 10;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Top 10 most viewed videos')
            st.write(df)

        elif question == '4. How many comments were made on each video, and what are their corresponding video names?':
            query = 'SELECT title, comments FROM videos;'
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Number of comments for each  video')
            st.write(df)

        elif question == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
            query = '''SELECT title, likes, channel_name
                       FROM videos
                       order by likes DESC;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Most liked videos')
            st.write(df)

        elif question == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
            query = 'SELECT title, likes FROM videos;'
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Number of likes for each  video')
            st.write(df)

        elif question == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
            query = '''SELECT SUM(views) channel_views, channel_name
                       FROM videos
                       GROUP BY channel_name
                       ORDER BY channel_views DESC;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Views of each channel')
            st.write(df)

        elif question == '8. What are the names of all the channels that have published videos in the year 2022?':
            query = '''SELECT DISTINCT(channel_name)
                       from videos
                       where published_date like '2022%';'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Channels which published videos in 2022')
            st.write(df)

        elif question == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
            query = '''SELECT channel_name, AVG(secs) average_duration
                        FROM(
                            SELECT channel_name,
                                   CASE WHEN duration REGEXP '^PT[0-9]+H[0-9]+M[0-9]+S$' 
                                        THEN time_to_sec(CONCAT(substring_index(substring_index(duration,'H',1),'T',-1),':',
                                             substring_index(substring_index(duration,'M',1),'H',-1),':',
                                             substring_index(substring_index(duration,'S',1),'M',-1)))
                                        WHEN duration REGEXP '^PT[0-9]+M[0-9]+S$' 
                                        THEN time_to_sec(CONCAT('0:',substring_index(substring_index(duration,'M',1),'T',-1),':',
                                             substring_index(substring_index(duration,'S',1),'M',-1)))
                                        WHEN duration REGEXP '^PT[0-9]+S$' 
                                        THEN time_to_sec(CONCAT('0:0:',substring_index(substring_index(duration,'S',1),'T',-1)))
                                        End as secs             
                            from videos) sub
                        GROUP BY channel_name
                        ORDER By average_duration DESC;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Average duration of a video from each channel')
            st.write(df)

        elif question == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
            query = '''SELECT title, channel_name, comments
                       FROM videos
                       ORDER BY comments DESC
                       LIMIT 10;'''
            mycursor.execute(query)

            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.header('Most commented videos')
            st.write(df)

elif options == 'About':
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write('### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')
