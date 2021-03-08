from random import randint

result = [0,0,0,0,0]
for i in range(1000):
    number = randint(0, (5*2)-1)
    if number % 2 == 0:
        print(f"Number {number}")
        result[number // 2] += 1
print(f"Result {result}")


