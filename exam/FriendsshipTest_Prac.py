questions = ["음악감상 vs 댄스",
             "떡볶이 vs 치킨",
             "바다 vs 산",
             "콜라 vs 사이다",
             "문자 vs 전화",
             "부먹 vs 찍먹",
             "오프라인 쇼핑 vs 온라인 쇼핑",
             "바나나 vs 딸기",
             "파랑 vs 노랑",
             "여름 vs 겨울" ]
jw_answers = ["댄스", "치킨", "바다", "콜라", "전화",
            "부먹", "온라인 쇼핑", "딸기",
            "파랑", "겨울"]

print("지동이를 얼만큼 알고 있어? 우정 테스트 시작!")

count = 0
for i in range(0, 10, 1):
    print("Q.", questions[i])
    result = input("선택지를 입력해주세요 : ")

    if jw_answers[i] == result:
        count += 1
        print("정답!", end='\n')
    else:
        print("틀렸어!", end='\n')

print(count, "개 맞췄습니다.")
if count >= 8:
    print("역시 나랑 제일 친한 친구야!")
elif count >= 4:
    print("괜찮아 더 알아가면 되지!")
elif count >= 0:
    print("나한테 관심 좀 갖어줘.")