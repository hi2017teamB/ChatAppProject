# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
#SQL文を実行する場合はself.execute_sql(sql)を呼ぶこと
BOT_ID = 5

def get_my_active_time(user):
	result = execute_sql("select Active_Time_start,Active_Time_end from user where name = '"+user+"'")
	active_time_text = result[0][0]+"~"+result[0][1]
	return active_time_text

def get_all_active_time():
	result = execute_sql("select Name,Active_Time_start,Active_Time_end from user")
	active_time=[]
	for i in result:
		active_time_text = i[0]+":"+i[1]+"~"+i[2]
		active_time.append(active_time_text)
	return active_time


def set_read_response(talk_id):
	execute_sql("update talk set Read_Res = 1 where Talk_ID = 'talk_id'")

def update_active_time(start,end,user):
	#print("update user set Active_time_start = ¥'"+start+"¥' Active_time_end= ¥'"+end+"¥' where name = "+user)
	execute_sql("update user set Active_time_start = '"+start+"' ,Active_time_end= '"+end+"' where name = '"+user+"'")

def get_active_time(resiever):
	result = execute_sql("select Active_Time_start,Active_time_end from \'user\' where Name= \""+ str(resiever)+"\"")
	print(result)
	active_time=[]
	for i in result:
		active_time.append(i)
	if len(i)!=2:
		return None
	else:
		return result

def delete_group(groupname):
	execute_sql("delete from \'Group\' where Name = \""+str(groupname)+"\"")

def insert_group(groupname,userlist):
	execute_sql("insert into \'Group\' (Name,User_ID) values(\""+str(groupname)+"\",\""+userlist+"\")")

def get_group_user_list(Group_id):
	result = execute_sql("select User_ID from \'group\' where Group_id = "+ str(Group_id))
	if len(result)!=1:
		return None
	user_list = result[0][0].split(',')
	return user_list

def get_message(to_id,from_id):
	execute_sql("update Talk set Read_User = \"" + to_id + "\" where From_id =" + from_id + " and To_id =" + to_id + " and Read_User IS NULL")
	return execute_sql("select * from talk where (To_id = "+to_id+" and From_id="+from_id+") or (To_id ="+from_id+" and From_id ="+to_id+") order by Talk_ID")

def get_group_message(group_id):
	return execute_sql("select * from talk where (To_id = "+group_id+") order by Talk_ID")

def get_now_time():
	return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

def get_user_list():
	result = execute_sql("select Name from User")
	user_list=[]
	for user in result:
		user_list.append(user[0])
	print(user_list)
	return user_list

def get_user_id_list():
	return execute_sql("select User_ID from User where User_ID <>" + str(BOT_ID))

def get_group_list():
	return execute_sql("select Name from \'Group\'")

def get_user_id(name,passwd):
	result = execute_sql("select User_id from User where Name = '" + name + "' and PassWord = '" + passwd +"'")
	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])

def get_user_id_from_name(name):
	result = execute_sql("select User_id from User where Name = '" + name+"'")
	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])

def get_group_id_from_name(name):
	result = execute_sql("select Group_id from \'Group\' where Name = '"+ name+"'")
	if(len(result) != 1):
		return None
	else:
		return str(result[0][0])

def get_group_name(id):
	result = execute_sql("select Name from \'Group\' where Group_id = '"+ str(id)+"'")
	if(len(result) != 1):
		return None
	else:
		return str(result[0][0])

def get_user_name_from_group(group_id):
	results = execute_sql("select User_ID from 'Group' where Group_ID = " + group_id)
	member_list = ""
	print("\n\n\n\n\n\\n\n\n\n\n\\n\n\n\n\n\n\\n\n\n\n\n")
	print(results)
	aa = results[0][0].split(",")
	print(aa)
	for a in aa:
		print(a)
		member_list += (get_user_name(a) + ",")

	return member_list[0:len(member_list)-1]


def get_user_name(user_id):
	result = execute_sql("select Name from User where User_id = " + str(user_id))

	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])


def insert_message(to_id, from_id, time, text, is_reserve):
	execute_sql("insert into Talk (\'to_id\', \'from_id\', time, text, is_reserve) values ("+str(to_id)+","+str(from_id)+",\""+time+"\",\""+text+"\","+str(is_reserve)+")")
	return

def get_user_from_grade(grade):
	result = execute_sql("select User_id from User where Grade = \"" + grade + "\"")
	return result

def get_all_from_bot():
	result = execute_sql("select * from bot;")
	return result

def get_is_in_lab(user_id):
	result = execute_sql("select Is_in_Lab from User where User_id = " + user_id)
	return result

def change_flag(bot_id, flag):
	result = execute_sql("update bot set Flag = " + str(flag) + " where Bot_id = " + str(bot_id))
	return

def get_unread_message_for_bot():
	result = execute_sql("select Text,from_id from Talk where To_id = " + str(BOT_ID) + " and (Read_User IS NULL or Read_User != \"" + str(BOT_ID) + "\")")
	a = execute_sql("update Talk set Read_User = \"" + str(BOT_ID) + "\" where To_id = \"" + str(BOT_ID) + "\" and (Read_User IS NULL or Read_User != \"" + str(BOT_ID) + "\")")
	return result

def insert_reminder(message, month, month_end, week, week_number, start_datetime, to, in_lab, flag):
	execute_sql("insert into Bot (Message, Month, Month_end, Week, Week_number, start_datetime, \'To\', In_Lab, Flag) values (\"" + message +"\","+ str(month) +","+ str(month_end) +","+ str(week) +","+ str(week_number) +",\""+ start_datetime +"\",\""+ to +"\","+ str(in_lab) +","+ str(flag) + ")")
	return

def change_start_datetime(bot_id, next_datetime):
	result = execute_sql("update bot set Start_datetime = \"" + next_datetime + "\" where Bot_id = " + str(bot_id))
	return

def get_in_lab_member():
	results = execute_sql("select Name from User where Is_in_Lab = 1")
	member_list = "研究室にいるメンバは"
	for result in results:
		member_list = member_list  + ", " + result[0]

	member_list += "です"

	return member_list



def execute_sql(sql):
	print(sql)
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.close()
	connector.commit()
	connector.close()
	return result




if __name__ == '__main__':
	None
