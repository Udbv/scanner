#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket, queue
import sys
import argparse
from threading import Thread
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from queue import Queue
import time

queue = Queue()

def createParser ():
    parser = argparse.ArgumentParser()#задаю аргументы для консоли
    parser.add_argument('-iL', '--hostname_file', default='hosts.txt',type = argparse.FileType())
    parser.add_argument('-p', '--ports_to_scan',  default='443,80,22,1723,445')
    parser.add_argument('-t', '--threads_count', default=100)
    parser.add_argument('-w', '--timeout_ms', default='200',type=float)
    parser.add_argument('-o', '--output_file', default='save.txt')

    return parser

output = []
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

host = namespace.hostname_file.readlines() #построчное считывание файла с хостами,правильно работает только с ip
ports = namespace.ports_to_scan.split(",")#считывание портов с расприделителем
threads = namespace.threads_count #кол-во потоков
pool = ThreadPool(threads)
timeout = (namespace.timeout_ms)/1000 #таймаут в мс
out = namespace.output_file#переменная с именем файла вывода
def scan ():
    for ip in range(len(host)):
        h = str(host[ip])#conntect воспринимает только str
        for port in ports:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(timeout)#задание таймаута
            try:
                result = c.connect_ex((h, int(port)))#создание подключения
                if result == 0:
                    print("ip", h , "Port {}:Open".format(port))#вывод в командную строку
                    output.append(str("\nip "+h+"Port {}:Open  ".format(port)))#запись в переменную

                else:
                    print('%s: port open %s' % (ip, port))
                    f = open(out, 'w')  # открытие файла для дозаписи
                    f.writelines(output)  # запись в файл
                    f.close()  # закрытие файла
                    c.close()  # закрытие сокета
            except:

                if result == True:
                    print('%s: port close %s' % (ip, port))
            pass
            queue.task_done()
scan()


if __name__==('__main__'):

    for i in range(threads):
        worker = Thread(target=scan(),args=(i,queue))
        worker.setDaemon(True)
        worker.start()
    for ip in host:
        queue.put(ip)
        print ('Main Thread Waititng ...')
        queue.join()
        print ('End of scan')


#asddddddddddd