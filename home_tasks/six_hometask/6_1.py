import re
first ='afoot, catfoot, dogfoot, fanfoot, foody, foolery, foolish, foster, footage, foothot, footle,footpad, footway, hotfoot, jawfoot, mafoo, nonfood, padfoot, prefool, sfoot, unfool'
second = 'Atlas, Aymoro, Iberic, Mahran, Ormazd, Silipan, altered, chandoo, crenel , crooked, fardo, folksy, forest, hebamic, idgah, manlike, marly, palazzo, sixfold, tarrock, unfold'

patter = re.compile('\w*foo\w*')
result = patter.findall(first)
print(result)

result = patter.findall(second)
print(result)

