from .Connection import Connection
from .AccessLayer import addUser

def dropAllTables():
    """This function removes all the tables from the database.
     If a new table is added make sure to update this function"""
    connection = Connection.createConnection()
    connection.execute_query("DROP TABLE IF EXISTS users;")
    connection.execute_query("DROP TABLE IF EXISTS user_types;")
    connection.execute_query("DROP TABLE IF EXISTS passwords;")
    connection.execute_query("DROP TABLE IF EXISTS astronaut_locations;")
    connection.execute_query("DROP TABLE IF EXISTS locations;")
    connection.execute_query("DROP TABLE IF EXISTS mfa_accounts;")
    connection.execute_query("DROP TABLE IF EXISTS items;")
    connection.execute_query("DROP TABLE IF EXISTS workout;")
    connection.commit()

def doesSchemaExist():
    rows = Connection.createConnection().execute_query("SELECT * FROM sqlite_master WHERE type='table'")
    if len(rows) >0:
        return True
    return False

def createTables():
    connection = Connection.createConnection()
    """This function adds all the tables from the database.
    pre-condition:Make sure the database is empty before calling this function.
    Call this before inserting or selecting any data.
    post-condition:All the required tables are created"""

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL UNIQUE,
      user_type TEXT NOT NULL,
      FOREIGN KEY (user_type) REFERENCES user_types(type)
    );
    """
    connection.execute_query(create_users_table)

    create_user_types_table = """
    CREATE TABLE IF NOT EXISTS user_types (
      type TEXT PRIMARY KEY NOT NULL
    );
    """
    connection.execute_query(create_user_types_table)

    create_passwords_table = """
    CREATE TABLE IF NOT EXISTS passwords (
      user_id INTEGER PRIMARY KEY ,
      password TEXT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
    connection.execute_query(create_passwords_table)

    create_locations_table = """
    CREATE TABLE IF NOT EXISTS locations (
      location TEXT PRIMARY KEY
    );
    """
    connection.execute_query(create_locations_table)

    create_astronaut_locations_table = """
        CREATE TABLE IF NOT EXISTS astronaut_locations (
          user_id INTEGER PRIMARY KEY ,
          location TEXT NOT NULL,
          FOREIGN KEY (user_id) REFERENCES users(id),
          FOREIGN KEY (location) REFERENCES locations(location)
        );
        """
    connection.execute_query(create_astronaut_locations_table)

    create_mfa_accounts_table = """
            CREATE TABLE IF NOT EXISTS mfa_accounts (
              email TEXT PRIMARY KEY,
              mfa_code TEXT NOT NULL,
              FOREIGN KEY (email) REFERENCES users(email)
            );
            """
    connection.execute_query(create_mfa_accounts_table)

    create_items_table = """
    CREATE TABLE IF NOT EXISTS items (
    	itemnumber INTEGER PRIMARY KEY AUTOINCREMENT,
    	itemdesc TEXT NOT NULL,
    	qtyonhand Integer NOT NULL,
    	minqty Integer NOT NULL
    	); """
    connection.execute_query(create_items_table)

    create_workout_table = """
    CREATE TABLE IF NOT EXISTS workout (
        workout_id INTEGER PRIMARY KEY,
        weight INTEGER NOT NULL,
        height INTEGER NOT NULL,
        workout_time TEXT NOT NULL,
        user DATE,
        FOREIGN KEY (user) REFERENCES users(email)
        );
    """
    connection.execute_query(create_workout_table)
    connection.commit()

    insertDefaultData()

def insertDefaultData():
    addDefaultValues()
    addUser('admin','password','ADMIN')

def addDefaultValues():
    connection = Connection.createConnection()
    insert_user_types = "INSERT INTO user_types (type) VALUES ('GROUND_CONTROL'), ('ASTRONAUT'), ('ADMIN');"
    connection.execute_query(insert_user_types)

    insert_locations = "INSERT INTO locations (location) VALUES ('EARTH'), ('FLYING'), ('SPACE_STATION');"
    connection.execute_query(insert_locations)

    insert_default_resources = "INSERT INTO items (itemdesc,qtyonhand,minqty) VALUES " \
                        "('Dried Apricot',200,100), ('Rehydrated Beef',100, 500), ('Dried Carrot',200,100), ('Oxygen',2500,1600);"
    connection.execute_query(insert_default_resources)
    connection.commit()