rand_num = [3, 8, 5, 9, 7, 4, 2, 6, 1]

for i in range(len(rand_num) - 1):
    for j in range(len(rand_num) - i - 1):
        if rand_num[j] > rand_num[j + 1]:
            rand_num[j], rand_num[j + 1] = rand_num[j + 1], rand_num[j]
            
print(rand_num)