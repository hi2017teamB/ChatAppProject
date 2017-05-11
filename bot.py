import db
import time
from datetime import datetime
import os


if __name__ == '__main__':
    while True:
        print (datetime.now().strftime('%Y/%m/%d %H:%M:%S'));
        print(str(db.get_user_from_grade("b4"))[0][0])
        time.sleep(1);
