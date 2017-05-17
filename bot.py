import db
import time
from datetime import datetime
from datetime import date
import os
import re
from syntax import Syntax

# def gomisute():
#     result = db.get_user_from_grade("b4")
#     text = "ゴミを捨てましょう"
#     for i in range(len(result)):
#         db.insert_message(result[i][0], BOT_ID, datetime.now().strftime('%Y%m%d%H%M%S'), text, 1)
#         print(result[i][0])

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
    if(flag == True and start_datetime.strftime("%H:%M") == now_datetime.strftime("%H:%M")):
    # if(flag == True and (start_datetime.strftime("%H") == now_datetime.strftime("%H"))):
        flag = True
    else:
        flag = False


    return flag

def enter_schedule():
    messages = db.get_unread_message_for_bot()
    for message in messages:
        find_datetime(message[0])
    print(messages)

# def find_time():

def find_datetime(message):
    # pattern = "^(?P<span>次の?|毎(週|月)|来週の?|来月の?|来年の?)?(?P<days>([0-9]{1,2}月[0-9]{1,2}日|[0-9]{1,2}日|末|第[1-5][日月火水木金土]曜[日]?)+)の？(?P<time>(午前|午後)[0-9]{1,2}時([0-9]{1,2}分)?|[0-9]{1,2}:[0-9]{1,2})に?(?P<lab>研究室にいる|研究室の)?((?P<grade>B4|M1|M2)|(?P<team>awareness|AWARENESS|novel\s?interface|NOVEL\s?INTERFACE|cmc|CMC))に？(?P<item>\S+)をリマインド$"
    pattern = "^(?P<span>次の?|毎(週|月)|来週の?|来月の?|来年の?)?(?P<days>([0-9]{1,2}月[0-9]{1,2}日|[0-9]{1,2}日|末|第[1-5][日月火水木金土]曜日?)+)の?(?P<time>(午前|午後)[0-9]{1,2}時([0-9]{1,2}分)?|[0-9]{1,2}:[0-9]{1,2})に?(?P<lab>研究室にいる|研究室の)?(?P<member>B4|M1|M2|awareness|AWARENESS|novel\s?interface|NOVEL\s?INTERFACE|cmc|CMC|全員|人)に?(?P<item>\S+)をリマインド$"
    match = re.search(pattern, message)

    if match:
        print("match")
        s = Syntax(match.group("span"), match.group("days"), match.group("time"), match.group("lab"), match.group("member"), match.group("item"))
        return s


    else:
        print("unmatch")
        return False


    # print(message)
    # pattern = "^(?P<span>次の?|毎(週|月)|来週の?|来月の?|来年の?)(?P<other>\S+)"
    # pattern2 = "^(([0-9]{4}年)?([1-9]|1[0-2])月)(([1-9]|[1-2][0-9]|3[0-1])日)(?P<other>\S+)"
    # match = re.search(pattern , message)
    # match2 = re.search(pattern2, message)
    # if match:
    #     other = match.group("other")
    #     if match.group("span") in {"毎月"}:
    #         print(match.group("span"))
    #         pattern = "^(?P<days>([0-9]{1,2}日|末|第[1-5][日月火水木金土]曜[日]?)+)(?P<other>\S+)"
    #         match = re.search(pattern , other)
    #         if match:
    #             other = match.group("other")
    #             days = match.group("days")
    #             print(match.group("days"))
    #             pattern = "[0-9]{1,2}日|末|第[1-5][日月火水木金土]曜[日]?"
    #             match_list = re.findall(pattern, days)
    #             print(match_list)
    #         else:
    #             print("構文エラー")
    #             return
    #
    #
    #     elif match.group("span") in {"毎週"}:
    #         print(match.group("span"))
    #         pattern = "(?P<days>([日月火水木金土]曜[日]?)+)(?P<other>\S+)"
    #         match = re.search(pattern , other)
    #         if match:
    #             other = match.group("other")
    #             days = match.group("days")
    #             print(match.group("days"))
    #             pattern = "[日月火水木金土]曜[日]?"
    #             match_list = re.findall(pattern, days)
    #             print(match_list)
    #         else:
    #             print("構文エラー")
    #             return
    #
    #     elif match.group("span") in {"次の", "次", "来週の", "来週"}:
    #         print(match.group("span"))
    #         pattern = "(?P<days>[日月火水木金土]曜[日]?)"
    #
    #     elif match.group("span") in {"来月の", "来月"}:
    #         print(match.group("span"))
    #         pattern = "(?P<days>[1-9]|[1-2][0-9]|3[0-1])日)"
    #
    #     elif match.group("span") in {"来年の", "来年"}:
    #         print(match.group("span"))
    #         pattern = "(?P<days>[日月火水木金土]曜[日]?)"
    #
    # elif match2:
    #     other = match2.group("other")
    # else:
    #     print("構文エラー")
    #     return
    #
    # pattern = "^の?(?P<time>\S*)に(?P<item>\S*)をリマインド$"
    # match = re.search(pattern, other)
    # if match:
    #     print(match.group("time"))
    #     print(match.group("item"))
    #     time = match.group("time")
    #     item = match.group("item")
    #     pattern = "^[0-2]?[0-9]:[0-5][0-9]$"
    #     pattern2 = "(午前|午後)[0-9]{1,2}時([0-9]{1,2}分|半)?"
    #     match = re.search(pattern, time)
    #     match2 = re.search(pattern2, time)
    #     if match:
    #         None
    #     elif match2:
    #         None
    #     else:
    #         print("構文エラー")
    #         return
    #
    # else:
    #     print("構文エラー")
    #     return


    # pattern = "^毎月(?P<day>(([0-9]{1,2}日)|末|(第[1-5][日月火水木金土]曜[日]?))+)に(?P<item>\S*)をリマインド"
    # # pattern = "^毎月([0-9]{1,2}日)([1-9]{1,2}日)に(?P<item>\S*)をリマインド"
    # match = re.search(pattern , message)
    # if match:
    #     print("毎月")
    #     print(match.group("day"))
    #     print(match.group("item"))
    # else:
    #     # print("matchFailed")
    #     None
    #
    # pattern = "^毎週(?P<day>([日月火水木金土]曜[日]?)+)に(?P<item>\S*)をリマインド"
    # match = re.search(pattern , message)
    # if match:
    #     print("毎週")
    #     print(match.group("day"))
    #     print(match.group("item"))
    # else:
    #     # print("matchFailed")
    #     None
    #
    # pattern = "^次の(?P<day>(([0-9]{1,2}日)|末|(第[1-5][日月火水木金土]曜[日]?))+)に(?P<item>\S*)をリマインド"
    # match = re.search(pattern , message)
    # if match:
    #     print("一回だけ")
    #     print(match.group("day"))
    #     print(match.group("item"))
    # else:
    #     # print("matchFailed")
    #     None




if __name__ == '__main__':
    while True:
        print (datetime.now().strftime('%Y/%m/%d %H:%M:%S'));
        # スケジュール登録メッセージを取得
        enter_schedule()

        # 送信スケジュールを取得
        results = db.get_all_from_bot()
        # print (results)
        for result in results:
            if(match_schedule(result) == True):
                if(result[7] == 1):
                    print("success")
                    members = []
                    # 送信先のidをリストmemberに
                    if(result[5].find('m') == 0 or result[5].find('b') == 0):
                        member_result = db.get_user_from_grade(result[5])
                        for m in member_result:
                            members.append(int(m[0]))
                    else:
                        tmp = r[5].split(",")
                        for i in range(len(tmp)):
                            members.append(int(tmp[i]))

                    # in_labの指定があれば
                    if(result[6] == 1):
                        tmp = []
                        for member in members:
                            if(db.get_is_in_lab(str(member))[0][0] == 1):
                                tmp.append(member)
                        members = tmp

                    print(members)
                    # メッセージ送信
                    for member in members:
                        db.insert_message(member, BOT_ID, datetime.now().strftime('%Y/%m/%d-%H:%M:%S'), result[1], 0)

                    db.change_flag(result[0], 0)

            else:
                if(result[7] == 0):
                    db.change_flag(result[0], 1)
                print("failed")
        # print (datetime.now().weekday())


        time.sleep(1);
