# -*- coding: utf-8 -*-
import sqlite3


def get_user_id(name,passwd):

	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("select User_id from User where Name = '" + name + "' and PassWord = '" + passwd +"'") 
	result = cursor.fetchall()

	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])
	cursor.close()
	connector.close()

def get_user_name(user_id):
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("select Name from User where User_id = " + user_id) 
	result = cursor.fetchall()

	if(len(result) !=1):
		print("not found")
		return None
	else:
		print(str(result[0][0]))
		return str(result[0][0])
	cursor.close()
	connector.close()


if __name__ == '__main__':
	get_user_passwd("")