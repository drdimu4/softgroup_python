import re
first = ['fu','tofu','snafu']
second = ['futz', 'fusillade', 'functional','discombobulated']

patter = re.compile('\w*fu(?!\w)')

result = patter.findall(second[1])
print(result)

