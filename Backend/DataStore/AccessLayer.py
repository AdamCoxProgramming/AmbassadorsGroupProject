from .Connection import Connection
from enum import Enum
from .Encryption import encryptString, decryptString

class Location(Enum):
    EARTH =0,
    FLYING =1,
    SPACE_STATION =2

ASTRONAUT = 'ASTRONAUT'
GROUND_CONTROL ='GROUND_CONTROL'
ADMIN ='ADMIN'

def getUserByEmail(email):
    connection = Connection.createConnection()
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id WHERE email = ? ;"
    userRows = connection.execute_query(select_user,[email])
    connection.commit()
    if len(userRows) == 0:
        return None
    #decrypt password
    listV = list(userRows[0])
    listV[4] = decryptString(userRows[0][4])
    return listV

def getUserById(id):
    connection = Connection.createConnection()
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id WHERE user_id = ? ;"
    userRows = connection.execute_query(select_user,[str(id)])
    connection.commit()
    if len(userRows) == 0:
        return None
    # decrypt password
    listV = list(userRows[0])
    listV[4] = decryptString(userRows[0][4])
    return listV

def getUsers():
    connection = Connection.createConnection()
    select_user = "SELECT * FROM users JOIN passwords ON users.id = passwords.user_id;"
    userRows = connection.execute_query(select_user)
    connection.commit()
    if len(userRows) == 0:
        return None
    # decrypt passwords
    lists = []
    for row in userRows:
        listV = list(row)
        listV[4] = decryptString(listV[4])
        lists.append(listV)
    return lists

def addUser(email,password,userType):
    connection = Connection.createConnection()
    insert_user = """INSERT INTO users (email,user_type) VALUES (?,?);"""
    id = connection.execute_query(insert_user,[email,userType])
    insert_password = """INSERT INTO passwords (password,user_id) VALUES (?,?);"""
    connection.execute_query(insert_password,[encryptString(password),str(id)])

    if userType == ASTRONAUT:
        groundLocationString = str(Location.EARTH).split('.')[1]
        insert_astronaut_location = """INSERT INTO astronaut_locations (location,user_id) VALUES (?,?);"""
        connection.execute_query(insert_astronaut_location,[groundLocationString,str(id)])
    connection.commit()
    return id

def setUserPassword(email,password):
    connection = Connection.createConnection()
    select_user_id = "SELECT id FROM users WHERE email =?"
    rows = connection.execute_query(select_user_id,[email])
    id = rows[0][0]
    update_password = "UPDATE passwords SET password = ? WHERE user_id = ? ;"
    connection.execute_query(update_password,[encryptString(password),str(id)])
    connection.commit()

def storeMfaId(email, mfaId):
    connection = Connection.createConnection()
    insert_mfa_account = """INSERT INTO mfa_accounts (email,mfa_code) VALUES (?,?);"""
    connection.execute_query(insert_mfa_account,[email,str(mfaId)])
    connection.commit()

def getMfaId(email):
    connection = Connection.createConnection()
    select_mfa_account = "SELECT mfa_code FROM mfa_accounts WHERE email =?"
    res = connection.execute_query(select_mfa_account,[email])
    connection.commit()
    return res[0][0]

def getAstronautLocation(email):
    connection = Connection.createConnection()
    select_location = "SELECT * FROM astronaut_locations JOIN users ON users.id = astronaut_locations.user_id WHERE email =?;"
    userLocationRows = connection.execute_query(select_location,[email])
    connection.commit()
    if len(userLocationRows) == 0:
        return None
    return userLocationRows[0][1]

def setAstronautLocation(location,email):
    connection = Connection.createConnection()
    select_user_id = "SELECT id FROM users WHERE email =?"
    rows = connection.execute_query(select_user_id,[email])
    id = rows[0][0]
    locationString = str(location).split('.')[1]
    update_location = "UPDATE astronaut_locations SET location = ? WHERE user_id = ?;"
    connection.execute_query(update_location,[locationString,str(id)])
    connection.commit()

def getItemStockQuantity(itemNumber):
    connection = Connection.createConnection()
    select_item_stock_quantity = "SELECT qtyonhand FROM items WHERE itemNumber =?;"
    rows = connection.execute_query(select_item_stock_quantity,[str(itemNumber)])
    connection.commit()
    return rows[0][0]

def consumeItemStock(itemNumber, quantity):
    connection = Connection.createConnection()
    update_item_quantity = "UPDATE items SET qtyonhand = qtyonhand - ? WHERE itemNumber  = ?;"
    connection.execute_query(update_item_quantity,[str(quantity), str(itemNumber)])
    connection.commit()

def getAllStockedItems():
    connection = Connection.createConnection()
    select_item_stock_quantity = "SELECT * FROM items;"
    res = connection.execute_query(select_item_stock_quantity)
    connection.commit()
    return res