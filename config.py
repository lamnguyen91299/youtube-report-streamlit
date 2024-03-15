# columns
video_table = ['channel_id', 'channel_name', 'video_id', 'type', 'video_title', 'video_description',
               'view_count', 'like_count', 'dislike_count', 'favoriteCount', 'commentCount',
               'publishedAt']

lottie_animation_url = 'https://assets8.lottiefiles.com/private_files/lf30_bntlaz7t.json'


# list of columns required
channel_id = []
channel_name = []
video_id = []
video_type = []
video_title = []
video_description = []
publishedAt = []
view_count = []
like_count = []
dislike_count = []
favoriteCount = []
commentCount = []

data = [channel_id, channel_name, video_id, video_type, video_title, video_description,
        publishedAt, view_count, like_count, dislike_count, favoriteCount, commentCount]


def reset_data():
    for item in data:
        item.clear()


