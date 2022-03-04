from psycopg2 import connect, sql, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

DB_NAME = "database_db"
DB_USER = 'postgres'
DB_PASSWORD = 'Cokol11wiek'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'


try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(f"""CREATE DATABASE {DB_NAME}""")
        print(f'Database {DB_NAME} created')
    except DuplicateDatabase:
        print(f'Database {DB_NAME} exists')
    cnx.close()
except OperationalError:
    print('Connection Error')
    raise ValueError('Connection Error')

create_user_table = sql.SQL(("""CREATE TABLE {table_name}(
    id SERIAL,
    username VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(80),
    PRIMARY KEY (id)
    );
    """).format(table_name='users'))

create_message_table = sql.SQL(("""CREATE TABLE IF NOT EXISTS {table_name}(
    id SERIAL,
    from_id INTEGER,
    to_id INTEGER,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(255),
    FOREIGN KEY (from_id) REFERENCES {table_name_foreign}(id) ON DELETE CASCADE,
    FOREIGN KEY (to_id) REFERENCES {table_name_foreign}(id) ON DELETE CASCADE
    );
    """).format(table_name='message', table_name_foreign='users'))

try:
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME)
        cnx.autocommit = True
        cursor = cnx.cursor()
        with cnx, cursor:
            try:
                cursor.execute(create_user_table)
                print('Table user created')
            except DuplicateTable as err:
                print(str(err).capitalize())

            try:
                cursor.execute(create_message_table)
                print('Table messages created')
            except DuplicateTable as err:
                print(str(err).capitalize())
    except OperationalError:
        print('Connection Error')
finally:
    cnx.close()
