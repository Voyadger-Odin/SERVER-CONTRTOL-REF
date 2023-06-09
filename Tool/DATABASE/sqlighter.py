#python.exe C:\Users\Lenovo\Documents\Projekts\Python\BOT\BOTAY_BOT\THE_BEST\DATABASE\sqlighter.py

import sqlite3
import json
import datetime
import os

from Tool import CONSTANTS

#==================================== Генератор токенов ====================================
def TokenGenerator(data):
	token = '{0}:{1}'.format(
		str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
		, data)
	return token
#===========================================================================================

def ensure_connection(func):
	def inner(*args, **kwargs):
		db_name = 'consoles.sqlite'
		db_path = f'{CONSTANTS.path_DataBase}/{db_name}'
		print(os.path.abspath(os.getcwd()))
		print(db_path)
		with sqlite3.connect(db_path) as conn:
			res = func(*args, conn = conn, **kwargs)
		return res
	return inner






@ensure_connection
def init_db_consoles(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS consoles')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS consoles (
			id 					INTEGER PRIMARY KEY,
			pid 				INTEGER NOT NULL,
			console_name 		TEXT NOT NULL,
			console_path 		TEXT NOT NULL,
			console_path_hash 	TEXT NOT NULL
		)
	''')

	# Сохранить изменения
	conn.commit()


@ensure_connection
def universal_db_edit(conn, query:str):
	cursor = conn.cursor()
	cursor.execute(query)


#============================================ Обработка пользователей ============================================


@ensure_connection
def add_new_console(conn, pid: int, console_name: str, console_path: str, console_path_hash: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO consoles (
				pid,
				console_name,
				console_path,
				console_path_hash
				) VALUES (?, ?, ?, ?)''',
				   (pid, console_name, console_path, console_path_hash,))


@ensure_connection
def has_console(conn, console_path_hash: str):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM consoles WHERE console_path_hash = ? LIMIT 1', (console_path_hash,))
	(find_console,) = cursor.fetchone()
	return (find_console > 0)


@ensure_connection
def close_console(conn, console_path_hash: str):
	cursor = conn.cursor()
	cursor.execute('DELETE FROM consoles WHERE console_path_hash = ?', (console_path_hash, ))
	conn.commit()

@ensure_connection
def get_all_console(conn):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM consoles')
	return cursor.fetchall()


#=================================================================================================================



#============================================ Обработка пользователей ============================================
@ensure_connection
def init_db_users(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS users')

	'''
	rule - Права
		* admin	- Администратор (Создавать пользователей)
		* developer - Разработчик (Создавать файлы)
		* observer - Наблюдатель (Только просматривать)
	'''

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id 					INTEGER PRIMARY KEY,
			login 				TEXT NOT NULL,
			password 			TEXT NOT NULL,
			rule 				TEXT NOT NULL DEFAULT ('observer')
		)
	''')

	# Сохранить изменения
	conn.commit()


@ensure_connection
def get_user(conn, id: int):
	cursor = conn.cursor()
	cursor.execute('SELECT id, login, rule FROM users WHERE id = ?', (id, ))
	user = cursor.fetchone()
	return user

@ensure_connection
def login_user(conn, login: str, password: str):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password, ))
	user = cursor.fetchone()
	return user


@ensure_connection
def get_all_users(conn):
	cursor = conn.cursor()
	cursor.execute('SELECT id, login, rule FROM users')
	return cursor.fetchall()

#=================================================================================================================


#======================================= STANDART QUEARY =======================================
# Получает указанное поле
@ensure_connection
def get_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str):
	'''
	table_name - название таблицы
	line - строка, которую нужно получить (например дату)
	line_selector - строка, по которой будем искать (например id)
	line_selector_value - значение, по которому будем искать
	'''
	cursor = conn.cursor()
	cursor.execute('SELECT {0} FROM {1} WHERE {2} = ?'.format(line, table_name, line_selector), (line_selector_value, ))

	data = cursor.fetchone()
	if (data != None):
		return data[0]
	else:
		return None


# Записывает информацию в указанное поле
@ensure_connection
def set_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str, data: str):
	cursor = conn.cursor()
	cursor.execute('UPDATE {0} SET {1} = {2} WHERE {3} = {4}'.format(table_name, line, data, line_selector, line_selector_value))
	conn.commit()
#===============================================================================================





@ensure_connection
def init_db(conn, force: bool = False):
	init_db_consoles(force=force)
	init_db_users(force=False)



if __name__ == '__main__':
	print('Соединение с базой')