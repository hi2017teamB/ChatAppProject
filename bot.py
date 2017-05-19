import db
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
# from datetime.time import time as dttime
import calendar
import os
import re
from syntax import Syntax
from dateutil.dateutil.relativedelta import relativedelta
from dateutil.dateutil.rrule import *
from dateutil.dateutil.parser import *

def match_schedule(r):
    flag = False
    now_datetime = datetime.now()
    str_datetime = r[6]
    start_datetime = datetime.strptime(str_datetime, '%Y/%m/%d-%H:%M:%S')

    # 当日
    if(start_datetime.date == now_datetime.date):
        flag = True

    # # 毎月
    # if(r[2] >= 0):
    #     if(start_datetime.day == now_datetime.day):
    #         flag = True
    #
    # # 毎週
    # if(r[4] >= 0):
    #     if(start_datetime.weekday == now_datetime.weekday):
    #         flag = True

    # 日付があって時刻もあってたら
    if(flag == True and start_datetime.strftime("%H:%M") == now_datetime.strftime("%H:%M")):
    # if(flag == True and (start_datetime.strftime("%H") == now_datetime.strftime("%H"))):
        flag = True
        f = 1
        if(r[3]>0):
            next_datetime = start_datetime + relativedelta(months=1)
        elif(r[4]>0):
            next_datetime = start_datetime + relativedelta(months=1, day=31)
        elif(r[5]>0):
            next_datetime = start_datetime + relativedelta(days=7)
        elif(r[6]>0):
            ns = start_datetime + relativedelta(months=1, day=1)
            ne = start_datetime + relativedelta(months=1, day=31)
            L = rrule(WEEKLY, byweekday=start_datetime.weekday, dtstart=ns, until=ne)
            next_datetime = L[r[6]]
            # print("yeah")
        else:
            f=0
            next_datetime = start_datetime

        nd = next_datetime.strftime("%Y/%m/%d-%H:%M:%S")
        db.change_start_datetime(r[0], nd)


    else:
        flag = False

    return flag


def enter_schedule():
    messages = db.get_unread_message_for_bot()
    for message in messages:
        print(message)
        s = syntax_matching(message[0])
        month, week, s_flag = span_flag(s.span)
        d_list, me_list, wn_list = calc_startday(s_flag, s.days)
        member = select_member(s.grade)
        is_in_lab = select_is_in_lab(s.in_lab)

        if d_list != False:
            print(d_list)

        t = calc_time(s.time)
        if t != False:
            print(t)

        input_datetime_list = [datetime.combine(d,t) for d in d_list]

        for (i, me, wn) in zip(input_datetime_list, me_list, wn_list):
            i_str = i.strftime('%Y/%m/%d-%H:%M:%S')
            db.insert_reminder(s.item, month, me, week, wn, i_str, member, is_in_lab, 1)



        # s.show_all()

def select_member(grade):
    if grade in {"人", "全員"} :
        return "everyone"
    elif grade in {"M1"}:
        return "m1"
    elif grade in {"M2"}:
        return "m2"
    elif grade in {"B4"}:
        return "b4"

def select_is_in_lab(in_lab):
    if in_lab in {"研究室にいる", "研究室の"} :
        return 1
    else:
        return 0

def calc_time(time):
    if ":" in time:
        pattern = "((?P<ap>am|AM|pm|PM)?)(?P<hour>[0-9]{1,2}):(?P<min>[0-9]{1,2})"
    else:
        pattern = "(?P<ap>(午前|午後)?)(?P<hour>[0-9]{1,2})時(?P<min>([0-9]{1,2}分)?)"

    match = re.search(pattern, time)
    ap = match.group("ap")
    h = int(match.group("hour"))
    # 空文字列をintにしない
    if match.group("min")!= "":
        m = int(match.group("min"))
    else:
        m = 0

    if ap in {"pm", "PM", "午後"}:
        h = h + 12

    try:
        dt = datetime(1995,1,1,h,m)
        input_time = dt.time()
        # input_time = datetime.time(h,m,0,0)
    except ValueError:
        return False

    return input_time


def calc_startday(s_flag, days):
    # span_flagが立ってない時正確な日付を求めるspa_flag = 0 すなわち次のor直接指定
    pattern = "[0-9]{1,2}月[0-9]{1,2}日|[0-9]{1,2}日|末|第[1-5][日月火水木金土]曜日?|[日月火水木金土]曜日?"
    days_list = re.findall(pattern, days)
    today = date.today()
    formatted_days_list = []
    month_end_list = []
    week_number_list = []
    s_month = today + relativedelta(day=1) #今月始
    ns_month = today + relativedelta(months=+1, day=1)
    e_month = today + relativedelta(day=31) #今月末
    ne_month = today + relativedelta(months=+1, day=31) #来月末

    for day in days_list:
        if "末" in day :
            # e_month = today + relativedelta(day=31)
            if today == e_month:
                e_month = ne_month

            formatted_days_list.append(e_month)
            month_end_list.append(1)
            week_number_list.append(0)
            # formatted_days_list.append(date(today.year, today.month, calendar.monthrange(today.year, today.month)[1]))

        elif "第" in day :
            pattern = "第(?P<num>[1-5])(?P<weekday>[日月火水木金土])曜日?"
            match = re.search(pattern, day)
            num = int(match.group("num"))
            week = "月火水木金土日".find(match.group("weekday"))
            L = rrule(WEEKLY, byweekday=week, dtstart=s_month, until=e_month)
            if L[num-1].date() <= today:
                L = rrule(WEEKLY, byweekday=week, dtstart=ns_month, until=ne_month)

            formatted_days_list.append(L[num-1].date())
            month_end_list.append(0)
            week_number_list.append(num)

        elif "曜" in day :
            pattern = "(?P<weekday>[日月火水木金土])曜日?"
            match = re.search(pattern, day)
            week = "月火水木金土日".find(match.group("weekday"))
            L = rrule(WEEKLY, byweekday=0, dtstart=today, until=ne_month)
            if L[0].date() <= today:
                formatted_days_list.append(L[1].date())
                month_end_list.append(0)
                week_number_list.append(0)
            else:
                formatted_days_list.append(L[0].date())
                month_end_list.append(0)
                week_number_list.append(0)

        elif "年" in day :
            pattern = "(?P<year>[0-9]{4})年(?P<month>[0-9]{1,2})月(?P<day>[0-9]{1,2})日"
            match = re.search(pattern, day)
            y = int(match.group("year"))
            m = int(match.group("month"))
            d = int(match.group("day"))
            try:
                input_day = date(y, m, d)
            except ValueError:
                return False
            formatted_days_list.append(input_day)
            month_end_list.append(0)
            week_number_list.append(0)
        elif "月" in day:
            pattern = "(?P<month>[0-9]{1,2})月(?P<day>[0-9]{1,2})日"
            match = re.search(pattern, day)
            m = int(match.group("month"))
            d = int(match.group("day"))
            try:
                input_day = date(today.year, m, d)
            except ValueError:
                return False

            if span_flag == 5 or (span_flag==0 and input_day <= today):
                try:
                    input_day = date(today.year+1, m, d)
                except ValueError:
                    return False

            formatted_days_list.append(input_day)
            month_end_list.append(0)
            week_number_list.append(0)

            # if span_flag == 5:
            #     try:
            #         input_day = date(today.year+1, m, d)
            #     except ValueError:
            #         return False
            # elif span_flag == 0 :
            #     try:
            #         input_day = date(today.year, m, d)
            #     except ValueError:
            #         return False
            #     if input_day <= today:
            #         input_day = date(today.year+1, m, d)
            #
            # else:
            #     try:
            #         input_day = date(today.year, m, d)
            #     except ValueError:
            #         return False
        elif "日" in day :
            try:
                input_day = date(today.year, today.month, d)
            except ValueError:
                return False
            if (span_flag ==0 or span_flag == 4) and input_day <= today:
                try:
                    input_day = date(today.year, today.month+1, d)
                except ValueError:
                    return False

            formatted_days_list.append(input_day)
            month_end_list.append(0)
            week_number_list.append(0)
        else:
            return False

    return (formatted_days_list, month_end_list, week_number_list)

def span_flag(span):
    if span in {"次", "次の"}:
        return [0,0,0]
    elif span in {"毎週"}:
        return [0,1,1]
    elif span in {"毎月"}:
        return [1,0,2]
    elif span in {"来週", "来週の"}:
        return [0,0,3]
    elif span in {"来月", "来月の"}:
        return [0,0,4]
    elif span in {"来年", "来年の"}:
        return [0,0,5]
    else:
        return False


def syntax_matching(message):
    pattern = "^(?P<span>次の?|毎(週|月)|来週の?|来月の?|来年の?)?(?P<days>([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日|[0-9]{1,2}月[0-9]{1,2}日|[0-9]{1,2}日|末|(第[1-5])?[日月火水木金土]曜日?)+)の?(?P<time>(午前|午後)?[0-9]{1,2}時([0-9]{1,2}分)?|(AM|PM|am|pm)?[0-9]{1,2}:[0-9]{1,2})に?(?P<lab>研究室にいる|研究室の)?(?P<member>B4|M1|M2|awareness|AWARENESS|novel\s?interface|NOVEL\s?INTERFACE|cmc|CMC|全員|人)に?(?P<item>\S+)をリマインド$"
    match = re.search(pattern, message)

    if match:
        print("match")
        s = Syntax(match.group("span"), match.group("days"), match.group("time"), match.group("lab"), match.group("member"), match.group("item"))
        return s
    else:
        print("unmatch")
        return False


if __name__ == '__main__':
    while True:
        print (datetime.now().strftime('%Y/%m/%d-%H:%M:%S'));
        print (datetime.now()  + relativedelta(months=1, day=1))
        # スケジュール登録メッセージを取得
        enter_schedule()

        # 送信スケジュールを取得
        results = db.get_all_from_bot()
        # print (results)
        for result in results:
            if(match_schedule(result) == True):
                if(result[9] == 1):
                    print("success")
                    members = []
                    # 送信先のidをリストmemberに
                    if(result[7].find('m') == 0 or result[7].find('b') == 0):
                        member_result = db.get_user_from_grade(result[7])
                        for m in member_result:
                            members.append(int(m[0]))
                    else:
                        member_result = db.get_user_id_list()
                        for m in member_result:
                            members.append(int(m[0]))
                        # tmp = r[5].split(",")
                        # for i in range(len(tmp)):
                        #     members.append(int(tmp[i]))

                    # in_labの指定があれば
                    if(result[8] == 1):
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
                if(result[9] == 0):
                    db.change_flag(result[0], 1)
                print("failed1")
        # print (datetime.now().weekday())


        time.sleep(1);
