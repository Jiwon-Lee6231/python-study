import json
import requests

import video_manage
import auth_manage

credentials = auth_manage.get_authenticated_google()
exercise_video = video_manage.get_exercise_video(credentials)
diet_video = video_manage.get_diet_video(credentials)

# 카카오 인증
kheaders = auth_manage.get_token("kakao")

# 카카오 리스트 템플릿(운동, 식단 2개)
kakao_temp = {
    "object_type": "list",
    "header_title": "오늘의 건돼있구",
    "header_link": {
        "web_url": exercise_video[0]['url'],
        "mobile_web_url": exercise_video[0]['url']
    },
    "contents": [
        {
            "title": exercise_video[0]['title'],
            "image_url": exercise_video[0]['img_url'],
            "link": {
                "web_url": exercise_video[0]['url'],
                "mobile_web_url": exercise_video[0]['url']
            }
        },
        {
            "title": diet_video[0]['title'],
            "image_url": diet_video[0]['img_url'],
            "link": {
                "web_url": diet_video[0]['url'],
                "mobile_web_url": diet_video[0]['url']
            }
        },
        {
            "title": diet_video[1]['title'],
            "image_url": diet_video[1]['img_url'],
            "link": {
                "web_url": diet_video[1]['url'],
                "mobile_web_url": diet_video[1]['url']
            }
        }
    ]
}

kakao_payload = {
    "template_object": json.dumps(kakao_temp)
}

kakao_template_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
kakao_res = requests.post(kakao_template_url, data=kakao_payload, headers=kheaders)

print(kakao_res.json())
