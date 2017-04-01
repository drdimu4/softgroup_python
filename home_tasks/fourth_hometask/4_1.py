import time
import random
from threading import Thread,Lock,RLock
def worker(file: object, i):
    ''' worker function writes two strings 
    with random pause to shared file using 
    synchronization
     primitive :param file: file-object :return: '''
    with lock:
        file.write('thread_'+str(i) + ': ' + 'started.\n')
        time.sleep(random.random() * 2)
        file.write('thread_'+str(i) + ': ' + 'done.\n')


if __name__ == '__main__':
    file = open('test.txt', 'a')
    lock = RLock()
    threads =[]
    for i in range(0,10):
        t = Thread(target=worker, args=(file,i))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

