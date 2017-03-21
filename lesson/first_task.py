class Lists:
    def __init__(self):
        self.a = []

    def conv(self,list):
        for each in list:
            if isinstance(each,int):
                self.a.append(each)
            else:
                self.conv(each)

    def print(self):
        print(self.a)

l = Lists()

l.conv([1,2,3,5,[6,7,[8,9]]])
l.print()

