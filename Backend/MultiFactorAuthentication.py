from authy.api import AuthyApiClient
from Backend.DataStore import AccessLayer

def registerMfaAccount(email,phoneNumber,countryCode):
    authy_api = AuthyApiClient(
        '44EeUVgvZ68tnvBVn8Jb331zMILxzkuX')  # This is the Authy secret ID, should be stored in the backend
    user = authy_api.users.create(
        email=email,
        phone=phoneNumber,
        country_code=countryCode)

    addMfaAccountId(email,user.id)

def addMfaAccountId(email,mfaId):
    AccessLayer.storeMfaId(email,mfaId)

def getUserMfaId(email):
    return AccessLayer.getMfaId(email)

def verifyMfaAccount(email,mfaCode):
    mfaId = getUserMfaId(email)
    authy_api = AuthyApiClient('44EeUVgvZ68tnvBVn8Jb331zMILxzkuX')
    verification = authy_api.tokens.verify(mfaId, token=mfaCode)
    return verification.ok()