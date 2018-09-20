import random

with open('SweetNothings.txt', encoding='utf-8') as f:
    a = f.readlines()
b = a[random.randint(0, len(a)-1)]
print(b)