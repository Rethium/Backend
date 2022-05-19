import sqlite3

# old queries
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, company TEXT);'
VALIDATE_USER = 'SELECT * FROM users WHERE name = ? AND password = ?;'
ADD_USER = 'INSERT INTO users (name, password, company) VALUES (?, ?, ?);'
GET_ALL_USERS = 'SELECT * FROM users;'
CHECK_IF_USER_EXISTS = 'SELECT * FROM users WHERE name = ? AND password = ? AND company = ?'

# new queries
INSERT_BEAN = 'INSERT INTO beans (name,method,rating) VALUES (?, ?, ?);'
GET_ALL_BEANS = 'SELECT * FROM beans'
GET_BEANS_BY_NAME = 'SELECT * FROM beans WHERE name = ?'
GET_BEST_PREPARATION_FOR_BEAN = 'SELECT * FROM beans WHERE name = ? ORDER BY rating DESC LIMIT 1'
GET_WORST_PREPARATION_FOR_BEAN = 'SELECT * FROM beans WHERE name = ? ORDER BY rating ASC LIMIT 1'
GET_COLUMN_NAMES = 'PRAGMA table_info(beans);'
GET_ALL_PREPARATION_METHODS = 'SELECT method FROM beans GROUP BY method'
CHECK_IF_ROW_EXISTS = 'SELECT * FROM beans WHERE name = ? AND method = ? AND rating = ?'

# new queries


def connect():
    return sqlite3.connect('data.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)


def validate_user(connection, username, password):
    with connection:
        return connection.execute(VALIDATE_USER, (username, password)).fetchone()


def add_user(connection, name, password, company):
    with connection:
        connection.execute(ADD_USER, (name, password, company))


def get_all_users(connection):
    with connection:
        return connection.execute(GET_ALL_USERS).fetchall()


def check_if_user_exists(connection, username, password, company):
    with connection:
        return connection.execute(CHECK_IF_USER_EXISTS,
                                  (username, password, company)).fetchone()

# ----------------------------------------------------------------------------------------------------------------------

# old queries


def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_BEAN, (name, method, rating))


def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()


def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()


def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN, (name,)).fetchone()


def get_worst_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN, (name,)).fetchone()


def get_column_names(connection):
    with connection:
        column_info = connection.execute(GET_COLUMN_NAMES).fetchall()
        columns = [entity[1] for entity in column_info]
        return columns


def get_all_preparation_methods(connection):
    with connection:
        return connection.execute(GET_ALL_PREPARATION_METHODS).fetchall()


def write_csv_header(connection):
    with open('data.csv', 'w+') as file:
        file.write(','.join(get_column_names(connection)) + '\n')
    file.close()


def export_database_to_csv(connection):
    with connection:
        all_data = connection.execute(GET_ALL_BEANS).fetchall()
        write_csv_header(connection)
        with open('data.csv', 'a') as file:
            for row in all_data:
                file.write(','.join(str(value) for value in row) + '\n')
        file.close()


def check_if_row_exists(connection, name, method, rating):
    with connection:
        return connection.execute(CHECK_IF_ROW_EXISTS,
                                  (name, method, rating)).fetchone()


def import_database_from_csv(connection):
    new_additions = 0
    with connection:
        with open('data.csv', 'r') as file:
            lines = file.readlines()
            del lines[0]
            for line in lines:
                line = line.strip().split(',')
                if(check_if_row_exists(connection, line[1], line[2], line[3]) == None):
                    add_bean(connection, line[1], line[2], line[3])
                    new_additions += 1
        file.close()
    write_csv_header(connection)
    return new_additions
