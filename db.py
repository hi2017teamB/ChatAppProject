# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
#SQL文を実行する場合はself.execute_sql(sql)を呼ぶこと
BOT_ID = 5


def get_message(to_id,from_id):
	return execute_sql("select * from talk where (To_id = "+to_id+" and From_id="+from_id+") or (To_id ="+from_id+" and From_id ="+to_id+") order by Talk_ID")


def get_now_time():
	return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

def get_user_list():
	return execute_sql("select Name from User")

def get_group_list():
	return execute_sql("select Name from \'Group_Info\'")

def get_user_id(name,passwd):
	result = execute_sql("select User_id from User where Name = '" + name + "' and PassWord = '" + passwd +"'")
	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])

def get_user_id(name):
	result = execute_sql("select User_id from User where Name = '" + name+"'")
	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])


def get_user_name(user_id):
	result = execute_sql("select Name from User where User_id = " + user_id)

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
	result = execute_sql("select Text from Talk where Talk.'To_id' = " + str(BOT_ID) + " and (Talk.Read_User IS NULL or Talk.Read_User != \"" + str(BOT_ID) + "\")")
	# a = execute_sql("update Talk set Read_User = \"" + str(BOT_ID) + "\" where Talk.'To' = \"" + str(BOT_ID) + "\" and (Talk.Read_User IS NULL or Talk.Read_User != \"" + str(BOT_ID) + "\")")
	return result



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
