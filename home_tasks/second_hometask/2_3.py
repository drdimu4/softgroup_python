import os

class MyOpen:
    def __init__(self,path,mode,encoding = 'utf-8'):
        self.path = path
        self.mode = mode
        self.encoding = encoding

        modes = {'r': os.O_RDONLY, 'w': os.O_WRONLY, 'a': os.O_APPEND, 'rw': os.O_RDWR, 'wa': os.O_APPEND}
        self.mode = modes.get(self.mode)
        if self.mode == None:
            self.mode = os.O_RDONLY

    def read(self,n=None):
        if (self.mode == os.O_RDONLY ) or (self.mode ==os.O_RDWR):
            return os.fdopen(os.open(self.path, self.mode)).read(n)

    def readLine(self):
        if (self.mode == os.O_RDONLY) or (self.mode == os.O_RDWR):
            f = os.fdopen(os.open(self.path, self.mode)).read()
            i = ''
            str = ''
            for char in f:
                if char=='\n':
                    break
                str+=char
            return str
    def write(self,s:str):
        if (self.mode == os.O_WRDONLY):
            f = os.open(self.path, self.mode)
            return os.write(f,s)
    def writeLine(self,s:str):
        if (self.mode == os.O_APPEND) or (self.mode == os.O_RDWR):
            f = os.open(self.path, self.mode)
            str='\n'
            str+=s
            return os.write(f,str)
    def clode(self):
        os.close(self)

#print(os.fdopen(os.open('new.txt', os.O_RDONLY)).read())
qwe = MyOpen('new.txt','')
print(qwe.read(10))
print(qwe.readLine())


