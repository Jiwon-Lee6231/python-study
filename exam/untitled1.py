import turtle as t

t.shape("turtle")
t.penup()
t.setx(-100)
t.sety(100)

t.forward(140)

# 'ㄴ' 쓰러 이동
t.penup()
t.left(180)
t.forward(140)

# 'ㄴ' 쓰기
t.pendown()
t.left(90)
t.forward(60)
t.left(90)
t.forward(140)

# 'ㅗ' 쓰러 이동
t.penup()
t.left(180)
t.forward(70)
t.left(90)

# 'ㅗ' 쓰기
t.pendown()
t.forward(40)

t.penup()
t.right(90)
t.forward(70)

t.pendown()
t.right(180)
t.forward(140)

t.penup()
t.right(180)
t.forward(70)
t.left(90)
t.forward(50)
t.left(90)

#한글은 왼쪽에서 오른쪽으로 'ㅇ'을 그림
t.pendown()
t.left(180)
t.circle(50)

# 0점으로 이동
t.penup()
t.home()