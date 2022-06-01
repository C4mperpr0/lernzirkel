import os
import shutil
from time import sleep
import datetime
from threading import Thread

if 'db_backup' not in os.listdir():
    os.mkdir('db_backup')

def backup():
    sleep(3)
    while 1:
        shutil.copy('lernzirkel.sqlite', f'db_backup/{round(datetime.datetime.now().timestamp())}')
        sleep(7200)
        # add autodeletion to prevent storage overflow!!!!!!!!!!!!!!!


t = Thread(target=backup)
t.start()
sleep(3)
print("Backup system started!")