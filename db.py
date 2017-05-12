# -*- coding: utf-8 -*-
import sqlite3


def get_user_list():
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("select Name from User")
	result = cursor.fetchall()
	cursor.close()
	connector.close()
	return result

def get_group_list():
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("select Name from GroupTable")
	result = cursor.fetchall()
	cursor.close()
	connector.close()
	return result



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

def insert_message(to_id, from_id, time, text, is_reserve):
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("insert into Talk (\'to\', \'from\', time, text, is_reserve) values ("+str(to_id)+","+str(from_id)+",\""+time+"\",\""+text+"\","+str(is_reserve)+")")
	# cursor.execute("insert into Talk (to, from, time, text, is_reserve) values ("+to_id+","+from_id+",\""+time+"\",\""+text+"\","+is_reserve+")")
	# cursor.execute("insert into talk(to, from, time, text, is_reserve) values(5, 5, \'19950204\', \'ゴミ捨て\', 1)")
	# cursor.execute("insert into Talk(From) values(5)")
	result = cursor.fetchall()

	connector.commit()

	cursor.close()
	connector.close()

def get_user_from_grade(grade):
	connector = sqlite3.connect("Chat.db")
	cursor = connector.cursor()
	cursor.execute("select User_id from User where Grade = \"" + grade + "\"")
	result = cursor.fetchall()

	return result

	cursor.close()
	connector.close()



if __name__ == '__main__':
	None
