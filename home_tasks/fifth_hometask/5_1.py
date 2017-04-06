import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', type = str,dest='l', help='Type your location')
parser.add_argument('-i',type=int, dest='id', help='Type your ID')

if __name__ == '__main__':

    args = parser.parse_args()
    URL = 'http://api.openweathermap.org/data/2.5/weather'
    q = args.l
    id = args.id
    appid = '7eea0dd982251635b57fe8f4082f3433'

    if (id is not None):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?{}{}&appid=7eea0dd982251635b57fe8f4082f3433'.format('id=',id))
    elif (q is not None):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?{}{}&appid=7eea0dd982251635b57fe8f4082f3433'.format('q=',q))
    else:
        print('Input right attributes')
        raise SystemExit(1)

    try:
        temp = r.json().get('main').get('temp')-273.15   #Перевод с Кельвинов в Цельсий
    except:
        print('Input right attributes')
        raise SystemExit(1)
    print(temp)



