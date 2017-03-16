def two(n:int):
    bin = ""
    while n>=1:
        bin+=str((n%2))
        n = int(n/2)
    return bin[::-1]
def eight(n:int):
    bin = ""
    while n>=1:
        bin+=str((n%8))
        n = int(n/8)
    return bin[::-1]
def six(n:int):
    asd = {'10':'A','11':'B','12':'C','13':'D','14':'E','15':'F'}
    bin = ""
    while n>=1:
        if str((n%16)) in asd.keys():
            bin+=asd.get(str(n%16))
        else:
            bin +=str(n%16)
        n = int(n/16)
    return bin[::-1]

def fine_print(n: int):
    for i in range(1,n+1):
        print('{0:<10}{1:10}{2:10}{3:10}'.format(i,eight(i),six(i),two(i)))

fine_print(15)