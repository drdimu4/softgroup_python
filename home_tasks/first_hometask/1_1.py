def like(numbers: str, a_set: str, b_set: str):
    n=numbers.split(' ')
    a=a_set.split(' ')
    b=b_set.split(' ')
    likes = 0
    for i in range(len(n)):
        if (n[i] in a) and (n[i] not in b):
            likes+=1
        if (n[i] in b) and (n[i] not in a):
            likes-=1
    return likes

numbers = '3 2 10 7 5 5 2 1 2'
a = '2 3 7'
b = '5 10 7'
print(like(numbers,a,b))
