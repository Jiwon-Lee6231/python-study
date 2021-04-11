from googleapiclient.discovery import build
from urllib.request import HTTPError

from datetime import date, timedelta

CLIENT_SECRETS_FILE = 'all_auth/client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events.readonly']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

def get_authenticated_service(credentials):
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# 스케줄 추가
# type : 운동, 식단
def insert_schedule(calendar, type, summary):
    calendar_id = 'primary'
    event = {
        'summary': '[' + type + ']' + summary,
        'description': type,
        'start': {
            'dateTime': date.today().isoformat() + 'T05:00:00+09:00',
            'timeZone': 'Asia/Seoul'
        },
        'end': {
            'dateTime': date.today().isoformat() + 'T23:00:00+09:00',
            'timeZone': 'Asia/Seoul'
        }
    }

    results = calendar.events().insert(calendarId=calendar_id, body=event).execute()

# 어제의 캘린더 정보 가져오기
def get_schedule_before(calendar, type):
    calendar_id = 'primary'
    before = (date.today() - timedelta(days=1)).isoformat()
    time_min = before + 'T00:00:00+09:00'
    time_max = before + 'T23:59:59+09:00'
    is_single_events = True
    orderby = 'startTime'

    try :
        events_results = calendar.events().list(calendarId = calendar_id,
                                              timeMin = time_min,
                                              timeMax = time_max,
                                              singleEvents = is_single_events,
                                              orderBy = orderby).execute()
    except HTTPError as e:
        return []

    results = []
    for item in events_results['items']:
        if (('식단' in item['summary']) and (type == '식단')) or (('운동' in item['summary']) and (type == '운동')):
            results.append(item['summary'])

    return results


# 한 주의 캘린더 정보 가져오기
def get_schedule_week(calendar, type):
    calendar_id = 'primary'
    first_day = (date.today() - timedelta(days=5)).isoformat()
    last_day = (date.today() - timedelta(days=1)).isoformat()
    date_min = first_day + 'T00:00:00+09:00'
    date_max = last_day + 'T23:59:59+09:00'
    is_single_events = True
    orderby = 'startTime'

    try:
        events_results = calendar.events().list(calendarId = calendar_id,
                                              timeMin = date_min,
                                              timeMax = date_max,
                                              singleEvents = is_single_events,
                                              orderBy = orderby).execute()
    except HTTPError as e:
        return []

    results = []
    for item in events_results['items']:
        if (('식단' in item['summary']) and (type == '식단')) or (('운동' in item['summary']) and (type == '운동')):
            results.append(item['summary'])

    return results
