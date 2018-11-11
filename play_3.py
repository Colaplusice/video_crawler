from utils import http_404_exception
from peewee import DoesNotExist

import time

for i in range(12):
    time.sleep(1)
    print(i)
    if i ==6:
        exec(1)
