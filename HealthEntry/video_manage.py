import random

from googleapiclient.discovery import build
import calendar_manage

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

playlist_ids = {
    'arms' : 'PLU6sdRtOqX3XcoFf994ZPo44REPgqxTQ4',
    'legs' : 'PLU6sdRtOqX3Vd3zuBkA1qM1piq_WIWHG1',
    'diet' : 'PLU6sdRtOqX3XYsoZzik4igXpy_VuRubfc'
}

CHANNEL_ID = 'UCDm6FjJmXJ_TRZqc8EIYvDw'

def get_authenticated_service(credentials):
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# 재생목록에 저장된 영상 목록 불러오기
def list_playlist_item(youtube, type, group=''):
    search_type = ''

    if type == '식단':
        search_type = 'diet'
    else:
        search_type = group

    item_results = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_ids[search_type]
    ).execute()

    results = []
    for item in item_results['items']:
        results.append(item)

    return results


# 영상 하나 불러오기
# 이번주 내에 추천된 영상인지 체크하기
def get_exercise_video(credentials):
    type = '운동'

    # 로그인
    youtube = get_authenticated_service(credentials)
    calendar = calendar_manage.get_authenticated_service(credentials)

    # 오늘의 7일 전까지의 운동 캘린더 데이터 가져오기
    calendar_week_data = calendar_manage.get_schedule_week(calendar, type)
    calendar_before_data = calendar_manage.get_schedule_before(calendar, type)
    arm_data = ['팔', '팔뚝살']
    file_format = ['son', 'seungha']
    file_name = 'My name is seungha'
    print(calendar_before_data[0])

    group = ''
    if len(calendar_before_data) == 0:
        group = 'arms'
    else:
        if any(format in calendar_before_data[0] for format in arm_data):
            group = 'legs'
        else:
            group = 'arms'

    # 영상 리스트 가져오기
    exercise_video_list = list_playlist_item(youtube, type, group)

    results = []
    list_len = len(exercise_video_list)
    while True:
        i = random.randrange(list_len)

        for data in calendar_week_data:
            if exercise_video_list[i]['snippet']['title'] == data[4:]:
                continue

        data_dic = {
            'title': exercise_video_list[i]['snippet']['title'],
            'img_url': exercise_video_list[i]['snippet']['thumbnails']['default']['url'],
            'url': 'https://www.youtube.com/watch?v={}&list={}'.format(exercise_video_list[i]['snippet']['resourceId']['videoId'], playlist_ids[group])
        }
        results.append(data_dic)

        if len(results) > 0:
            calendar_manage.insert_schedule(calendar, type, exercise_video_list[i]['snippet']['title'])
            break

    return results

# 식단영상
def get_diet_video(credentials):
    type = '식단'

    # 로그인
    youtube = get_authenticated_service(credentials)
    calendar = calendar_manage.get_authenticated_service(credentials)

    # 오늘의 7일 전까지의 식단 캘린더 데이터 가져오기
    diet_week_data = calendar_manage.get_schedule_week(calendar, type)
    diet_before_data = calendar_manage.get_schedule_before(calendar, type)

    # 영상 리스트 가져오기
    diet_video_list = list_playlist_item(youtube, type)

    results = []
    list_len = len(diet_video_list)
    while True:
        i = random.randrange(list_len)

        for data in diet_before_data:
            if diet_video_list[i]['snippet']['title'] == data[4:]:
                continue

        for data in diet_week_data:
            if diet_video_list[i]['snippet']['title'] == data[4:]:
                continue

        if len(results) > 0 and results[0]['title'] == diet_video_list[i]['snippet']['title']:
            continue

        data_dic = {
            'title': diet_video_list[i]['snippet']['title'],
            'img_url': diet_video_list[i]['snippet']['thumbnails']['default']['url'],
            'url': 'https://www.youtube.com/watch?v={}&list={}'.format(diet_video_list[i]['snippet']['resourceId']['videoId'], playlist_ids['diet'])
        }
        results.append(data_dic)
        calendar_manage.insert_schedule(calendar, type, diet_video_list[i]['snippet']['title'])

        if len(results) == 2:
            break

    return results