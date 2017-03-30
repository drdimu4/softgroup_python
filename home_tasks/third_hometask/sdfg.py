with open('csv.txt','r') as file:
    s = file.read()
    new=''
    for char in s:
        if char==';':
            new+=' '
        else :
            new+=char
    print(new)

with open('json.txt','r') as file:
    dict = eval(file.read())
    new=''
    for each in dict.get('rows'):
        new+=each+'\n'
    print(new)

with open('csv.txt','w') as file:
    file.write(new)
print(open('csv.txt','r').read())



