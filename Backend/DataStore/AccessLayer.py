from .Connection import Connection
from enum import Enum

class AccountTypes(Enum):
    ASTRONAUT = 'ASTRONAUT',
    GROUND_CONTROL ='GROUND_CONTROL',
    ADMIN ='ADMIN'

def getUserByEmail(email):
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id WHERE email ='" + email +"' ;"
    userRows = Connection.connection.execute_query(select_user)
    if len(userRows) == 0:
        return None
    return userRows[0]

def addUser(email,password,userType):
    insert_user = """INSERT INTO users (email,user_type) VALUES (""" + "'" + email + "'," + "'" + str(userType) + "'" + ");"
    id = Connection.connection.execute_query(insert_user)
    insert_password = """INSERT INTO passwords (password,user_id) VALUES (""" + "'" + password + "'," +  str(id) + ");"
    Connection.connection.execute_query(insert_password)
    return id

def setUserPassword(email,password):
    select_user_id = "SELECT id FROM users WHERE email ='" + email + "'"
    rows = Connection.connection.execute_query(select_user_id)
    id = rows[0][0]
    update_password = "UPDATE passwords SET password = '" +password + "' WHERE user_id = " + str(id) + ";"
    Connection.connection.execute_query(update_password)