import db
import time
from datetime import datetime
import os

BOT_ID = 5

# def gomisute():


if __name__ == '__main__':
    while True:
        print (datetime.now().strftime('%Y/%m/%d %H:%M:%S'));
        result = db.get_user_from_grade("m1")
        text = "ゴミを捨てましょう"
        for i in range(len(result)):
            db.insert_message(result[i][0], BOT_ID, datetime.now().strftime('%Y%m%d%H%M%S'), text, 1)
            print(result[i][0])

        time.sleep(1);
