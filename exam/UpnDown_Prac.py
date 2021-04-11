import random

rand_num = random.randrange(1, 71, 1)
num = 0
cnt = 0

print("[ 1 ~ 70 Up & Down 게임 ]");

while rand_num != num:
    num = int(input("1 ~ 70 사이의 숫자를 입력하세요 : "))

    if num < 1 and n > 70:
        print("1부터 70까지만 입력해주세요.")
    elif num > rand_num:
        print("Down!!")
    elif num < rand_num:
        print("Up!!")

    cnt += 1
    
print("---------------------");
print(cnt, "번 만에 맞췄습니다.")