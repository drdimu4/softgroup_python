from abc import ABC, abstractmethod


def csv_load(file: object) -> str:
    s = file.read()
    new = ''
    for char in s:
        if char == ';':
            new += ' '
        else:
            new += char
    return new


def csv_save(s:str, file:object) -> None:
    file.write(s)


def json_load(file:object) -> str:
    dict = eval(file.read())
    new = ''
    for each in dict.get('rows'):
        new += each + '\n'
    return new


def json_save(s:str, file:object) -> None:
    file.write(s)


class AbsConverterFabric(ABC):

    @abstractmethod
    def create_converter(self, _from: str, _to :str) -> object:
        raise NotImplemented


class AbstractConverter(ABC):

    @abstractmethod
    def load(self, file:object) ->str:
        raise NotImplemented

    @abstractmethod
    def save(self, s: str, file:object) -> object:
        raise NotImplemented

class ConverterFabric(AbsConverterFabric):                              #Я так и не понял как заставить
    def create_converter(self, _from: str, _to: str) -> object:         #обьект применять нужные функции(((
        self._from = _from                                              #Но конвертация вроде как робочая))
        self._to = _to                                                  #
        return self


if __name__ == '__main__':
    fab = ConverterFabric()
    converter1 = fab.create_converter('csv','json')
    converter2 = fab.create_converter('json','csv')

    with open('csv.txt','r') as file:
        result = converter1.load(file)
        print(result)

    print()

    with open('json.txt','w') as file:
        converter1.save(result,file)

    with open('json.txt','r') as file:
        result = converter2.load(file)
        print(result)

    with open('csv.txt', 'w') as file:
        converter2.save(result, file)
