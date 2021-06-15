from .Connection import Connection

def dropAllTables():
    """This function removes all the tables from the database.
     If a new table is added make sure to update this function"""
    Connection.connection.execute_query("DROP TABLE IF EXISTS users;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS user_types;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS passwords;")

def doesSchemaExist():
    rows = Connection.connection.execute_query("SELECT * FROM sqlite_master WHERE type='table'")
    if len(rows) >0:
        return True
    return False

def createTables():
    """This function adds all the tables from the database.
    pre-condition:Make sure the database is empty before calling this function.
    Call this before inserting or selecting any data.
    post-condition:All the required tables are created"""

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      user_type TEXT NOT NULL,
      FOREIGN KEY (user_type) REFERENCES user_types(type)
    );
    """
    Connection.connection.execute_query(create_users_table)

    create_user_types_table = """
    CREATE TABLE IF NOT EXISTS user_types (
      type TEXT PRIMARY KEY NOT NULL
    );
    """
    Connection.connection.execute_query(create_user_types_table)

    create_passwords_table = """
    CREATE TABLE IF NOT EXISTS passwords (
      user_id INTEGER PRIMARY KEY ,
      password TEXT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
    Connection.connection.execute_query(create_passwords_table)

    insertDefaultData()

def insertDefaultData():
    insert_user_types = "INSERT INTO user_types (type) VALUES ('GROUND_CONTROL'), ('ASTRONAUT'), ('ADMIN');"
    Connection.connection.execute_query(insert_user_types)