import db
import time
from datetime import datetime
from datetime import date
import os

BOT_ID = 5

def gomisute():
    result = db.get_user_from_grade("b4")
    text = "ゴミを捨てましょう"
    for i in range(len(result)):
        db.insert_message(result[i][0], BOT_ID, datetime.now().strftime('%Y%m%d%H%M%S'), text, 1)
        print(result[i][0])

def match_schedule(r):
    flag = False
    now_datetime = datetime.now()
    str_datetime = r[4]
    start_datetime = datetime.strptime(str_datetime, '%Y/%m/%d-%H:%M:%S')

    # 当日
    if(start_datetime.date == now_datetime.date):
        flag = True


    # 毎月
    if(r[2] >= 0):
        if(start_datetime.day == now_datetime.day):
            flag = True

    # 毎週
    if(r[3] >= 0):
        if(start_datetime.weekday == now_datetime.weekday):
            flag = True

    # 日付があって時刻もあってたら
    # if(flag == True and start_datetime.strftime("%H:%M") == now_datetime.strftime("%H:%M")):
    if(flag == True and (start_datetime.strftime("%H") == now_datetime.strftime("%H"))):
        flag = True
    else:
        flag = False


    return flag



if __name__ == '__main__':
    while True:
        print (datetime.now().strftime('%Y/%m/%d %H:%M:%S'));
        result = db.get_all_from_bot()
        print (result)
        for r in result:
            if(match_schedule(r) == True):
                print("success")
                members = []
                # 送信先のidをリストmemberに
                if(r[5].find('m') == 0 or r[5].find('b') == 0):
                    member_result = db.get_user_from_grade(r[5])
                    for m in member_result:
                        members.append(int(m[0]))
                else:
                    tmp = r[5].split(",")
                    for i in range(len(tmp)):
                        members.append(int(tmp[i]))

                # in_labの指定があれば
                if(r[6] == 1):
                    tmp = []
                    for member in members:
                        if(db.get_is_in_lab(str(member))[0][0] == 1):
                            tmp.append(member)
                    members = tmp

                print(members)
                # メッセージ送信
                for member in members:
                    db.insert_message(member, BOT_ID, datetime.now().strftime('%Y/%m/%d-%H:%M:%S'), r[1], 0)
            else:
                print("failed")
        # print (datetime.now().weekday())


        time.sleep(1);
