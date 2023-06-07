import sqlite3


# ======================================= STANDART QUEARY =======================================
# Список таблиц
def get_tables(path_db: str):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = []
        for item in cursor.fetchall():
            result.append(item[0])

        return result

# Список колонок (с типами данных) таблицы
def get_tableColumns(path_db: str, table: str):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(f'pragma table_info({table});')

        return cursor.fetchall()

# Данные таблицы
def get_tableData(path_db: str, table: str):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table};')

        return cursor.fetchall()

# ===============================================================================================
