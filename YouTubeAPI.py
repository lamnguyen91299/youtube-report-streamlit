from googleapiclient.discovery import build
import googleapiclient.discovery
import config
import util
import streamlit as st
import encrypt as e
import os

# Check if the app is running in Streamlit Cloud
if "openai_api_key" in st.secrets and "youtube_api_key" in st.secrets:
    # Use Streamlit Secrets if running in Streamlit Cloud
    openai_api_key = st.secrets["openai_api_key"]
    youtube_api_key = st.secrets["youtube_api_key"]
else:
    # Load environment variables if running locally
    from dotenv import load_dotenv
    import os
    load_dotenv()
    openai_api_key = os.getenv("openai_api_key")
    youtube_api_key = os.getenv("youtube_api_key")



# youtube = build('youtube', 'v3', developerKey=os.environ['API_KEY'])
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def get_channel_videos(channel_id):
    """Fetch the list of videos present under the channel id.

    :param channel_id: youtube channel id of the user
    :return : list of videos

    """
    res = youtube.channels().list(id=channel_id,
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None
    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos


def get_videos_stats(video_id):
    """Fetch the statistics corresponding to the provided video id.

    :param video_id : youtube video id
    :return stats: statistics of video
    """
    stats = []
    st.markdown(""" ##### Preparing required data.... """)
    my_bar = st.progress(1)
    for i in range(0, len(video_id)):
        res = youtube.videos().list(id=video_id[i],
                                    part='statistics').execute()
        stats += res['items']
        value_ = (i / len(video_id))
        my_bar.progress(value_)
        if i == len(video_id) - 1:
            diff = 1 - value_
            my_bar.progress(value_ + diff)

    return stats


def video_table(list_of_videos):
    """Fetch the list of videos present under the channel id.

    :param list_of_videos: list of videos
    :return : list of videos
    """
    st.markdown(""" ##### Getting videos .... """)
    my_bar = st.progress(1)
    i = 1
    for video in list_of_videos:
        my_bar.progress(i/len(list_of_videos))
        i += 1
        config.channel_id.append(video['snippet']['channelId'])
        config.channel_name.append(video['snippet']['channelTitle'])
        config.video_id.append(video['snippet']['resourceId']['videoId'])
        config.video_type.append(video['snippet']['resourceId']['kind'])
        config.video_title.append(video['snippet']['title'])
        config.video_description.append(video['snippet']['description'])
        config.publishedAt.append(video['snippet']['publishedAt'])


def stat_table(video_stats):
    """Joins all the required columns.

    :param video_stats : list of videos
    :return : no value
    """
    st.markdown(""" ##### Generating statistics...  """)
    my_bar = st.progress(1)
    i = 1
    for stat in video_stats:
        my_bar.progress(i / len(video_stats))
        i += 1
        if util.key_in_dict_and_not_none(stat['statistics'], "viewCount"):
            config.view_count.append(stat['statistics']['viewCount'])
        else:
            config.view_count.append(0)
        if util.key_in_dict_and_not_none(stat['statistics'], "likeCount"):
            config.like_count.append(stat['statistics']['likeCount'])
        else:
            config.like_count.append(0)
        if util.key_in_dict_and_not_none(stat['statistics'], "dislikeCount"):
            config.dislike_count.append(stat['statistics']['dislikeCount'])
        else:
            config.dislike_count.append(0)
        if util.key_in_dict_and_not_none(stat['statistics'], "favoriteCount"):
            config.favoriteCount.append(stat['statistics']['favoriteCount'])
        else:
            config.favoriteCount.append(0)
        if util.key_in_dict_and_not_none(stat['statistics'], "commentCount"):
            config.commentCount.append(stat['statistics']['commentCount'])
        else:
            config.commentCount.append(0)

def get_channel_avatar(channel_id):
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=e.decrypt('FNefXdF1I8IQZblmf9e2EpOdVTRXvK27yMH7WKp',5))

    request = youtube.channels().list(
        part='snippet',
        id=channel_id
    )
    response = request.execute()

    try:
        thumbnail_url = response['items'][0]['snippet']['thumbnails']['high']['url']
        return thumbnail_url
    except (KeyError, IndexError):
        return None
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
