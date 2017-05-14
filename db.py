# -*- coding: utf-8 -*-
import sqlite3

#SQL文を実行する場合はself.execute_sql(sql)を呼ぶこと

def get_user_list():
	return execute_sql("select Name from User")

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

def get_user_name(user_id):
	result = execute_sql("select Name from User where User_id = " + user_id)

	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])


def insert_message(to_id, from_id, time, text, is_reserve):
	execute_sql("insert into Talk (\'to\', \'from\', time, text, is_reserve) values ("+str(to_id)+","+str(from_id)+",\""+time+"\",\""+text+"\","+str(is_reserve)+")")
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
