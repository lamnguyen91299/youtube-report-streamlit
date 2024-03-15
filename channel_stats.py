import pandas as pd
import streamlit as st
import YouTubeAPI as youTube
import config
import plotly.express as px
import generate_sumary as gs
from numerize import numerize

# set the layout of the app
st.set_page_config(layout='wide')


# load animation
# load_animation = util.load_lottieurl(config.lottie_animation_url)
# st_lottie(load_animation, height=200)


# set the title of the app
st.title('Youtube channel auto report')

with st.expander('About this app'):
    st.write('This is a data collection app which allows users to download the list of videos posted by YouTube Channel '
             'using YouTube API.')


# hide the sidebar
st.markdown(""" <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """,
            unsafe_allow_html=True)


with st.form('youTube_channel_id'):
        youTubeChannelID = st.text_input(label='YouTube Channel ID', placeholder='Paste the youtube channel id here...for '
                                                                             'eg. UCSNeZleDn9c74yQc-EKnVTA',
                                     help="To test the app you can use channel id UCSNeZleDn9c74yQc-EKnVTA")
        st.form_submit_button(label='Get Channel Stats')
        st.write('Use this Channel Id : UC6bXz3g1C9H6bdFa-wcZ72Q')
        st.write('if you dont have any :)')

if youTubeChannelID == '':
    st.stop()
else:
    list_of_videos = youTube.get_channel_videos(youTubeChannelID)
    youTube.video_table(list_of_videos)
    video_stats = youTube.get_videos_stats(config.video_id)
    youTube.stat_table(video_stats)
    df = pd.DataFrame(zip(config.channel_id, config.channel_name,
                          config.video_id, config.video_type, config.video_title,
                          config.video_description, config.view_count, config.like_count,
                          config.dislike_count, config.favoriteCount, config.commentCount,
                          config.publishedAt), columns=config.video_table)

    st.markdown(""" ## YouTube Channel Details """)
    st.write('Channel Name: ', config.channel_name[0])

    # metrics
    total_videos, total_views, total_likes, total_comments = st.columns(4)
    total_videos.metric("Total Videos", len(config.video_id))
    total_views.metric("Total Views", numerize.numerize(float(df['view_count'].astype(int).sum()), 2))
    total_likes.metric("Total Likes", numerize.numerize(float(df['like_count'].astype(int).sum()), 2))
    total_comments.metric("Total Comments", numerize.numerize(float(df['commentCount'].astype(int).sum()), 4))

    # display dataframe
    st.dataframe(df.head(100))
    # Download data
    csv = youTube.convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{config.channel_name[0]}.csv',
        mime='text/csv',
    )
    #sumary data
    df_short = df[['channel_id', 'channel_name', 'video_id', 'type', 'video_title',
               'view_count', 'like_count', 'dislike_count', 'favoriteCount', 'commentCount',
               'publishedAt']]

    msg_sumary_data = gs.generate_summary_dataframe(df_short)

    st.write('Summary: ', msg_sumary_data)
    # visualization
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['year'] = df['publishedAt'].dt.year
    df['month'] = df['publishedAt'].dt.month
    df['week'] = df['publishedAt'].dt.isocalendar().week

    videos_per_year = df.groupby('year')['video_id'].count().reset_index()
    videos_per_year.columns = ['Year', 'Count']
    fig_videos_per_year = px.bar(videos_per_year, x='Year', y='Count', title='Videos posted per Year')
    st.plotly_chart(fig_videos_per_year)

    # reset the data
    config.reset_data()


