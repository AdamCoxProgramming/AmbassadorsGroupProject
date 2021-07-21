import ApiMode
import Backend.Schedular as Schedular

if __name__ == '__main__':
    ApiMode.ApiSetting.runningServerOnly = True
    Schedular.Schedular.start()

import logging
from Backend.Monitoring import getNumberOfCallInLastXMins
import json
import pickle
from flask import Flask, app, request
from flask_restful import Api, Resource, reqparse
from ApiMode import ApiSetting
from Backend import ISS
from Backend.Accounts import UserAccounts, isCorrectPassword, addUserAccount
from Backend.MultiFactorAuthentication import registerMfaAccount, verifyMfaAccount
from Backend.Resources import Resources
from Backend.ServerAPI import IssState

apiSecretKey = 'ag5Q0n>Oa<xa@41'

def pickleObject(object):
    pickled = pickle.dumps(object, 0)
    return pickled.decode('utf-8')

class Iss(Resource):
    def get(self):
        return pickleObject(IssState(ISS.getIssOxogenLevel())), 201

class Shuttles(Resource):
    def get(self):
        return pickleObject(ISS.getStatesOfShuttles()), 201

class ShuttlesLocation(Resource):
    #def get(self,shuttleNumber):
    #    return pickleObject(ISS.isShuttleOnEarth(shuttleNumber)), 201
    def post(self,shuttleNumber):
        parser = reqparse.RequestParser()
        parser.add_argument("astronautIds")
        args = parser.parse_args()
        astronautIds = json.loads(args["astronautIds"])
        ISS.launchShuttleToAppropriateDestination(int(shuttleNumber), astronautIds)
        return {}, 201

class ResourceItem(Resource):
    def get(self,itemNumber):
        try:
            return Resources.getItemStockQuantity(int(itemNumber)), 201
        except:
            return {},501

    def put(self,itemNumber):
        parser = reqparse.RequestParser()
        parser.add_argument("itemNumber")
        parser.add_argument("amountToConsume")
        args = parser.parse_args()
        Resources.consumeItemStock(int(itemNumber),int(args["amountToConsume"]))
        return {}, 201

class ResourceItems(Resource):
    def get(self,):
        pickled = pickleObject(Resources.getAllStockedItems())
        return pickled, 201

class Astronauts(Resource):
    def get(self):
        pickled = pickleObject(ISS.getAstronauts())
        return pickled, 201

class User(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        args = parser.parse_args()
        pickled = pickleObject(UserAccounts().getUserAccountByEmail(args["email"]))
        return pickled, 201

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("type")
        args = parser.parse_args()
        try:
            addUserAccount(args["email"], args["type"])
            return {}, 201
        except:
            return {},501

class Password(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()

        isCorrect = isCorrectPassword(args["email"],args["password"] )
        apiKey = None
        if isCorrect:
            apiKey = apiSecretKey
        pickled = pickleObject({"passwordMatch": isCorrect, "apiKey": apiKey })
        return pickled, 201

class MFA(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("mfaCode")
        args = parser.parse_args()
        return pickleObject(verifyMfaAccount(args["email"], args["mfaCode"])), 201
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("phone")
        parser.add_argument("countryCode")
        args = parser.parse_args()
        registerMfaAccount(args["email"], args["phone"], args["countryCode"])
        return {}, 201

class Monitor(Resource):
    def get(self):
        return pickleObject(getNumberOfCallInLastXMins(15)), 201

if ApiSetting.distrubuted:
    app = Flask(__name__)
    api = Api(app)

    @app.before_request
    def before_request():
        keyRequired = True
        if request.endpoint == 'user' and request.method =='GET':
            keyRequired = False
        elif request.endpoint == 'password' and request.method =='GET':
            keyRequired = False

        if keyRequired:
            if request.headers['apiKey'] != apiSecretKey:
                return "denied", 501

    api.add_resource(ResourceItem, "/ResourceItem/<itemNumber>")
    api.add_resource(ResourceItems, "/ResourceItems/")
    api.add_resource(Iss, "/Iss/")
    api.add_resource(Shuttles, "/Shuttles/")
    api.add_resource(ShuttlesLocation, "/ShuttlesLocation/<shuttleNumber>")
    api.add_resource(Astronauts, "/Astronauts/")
    api.add_resource(User, "/User/")
    api.add_resource(Password, "/Password/")
    api.add_resource(MFA, "/MFA/")
    api.add_resource(Monitor, "/Monitor/")

    logging.basicConfig(filename='api_logs.txt', level=logging.DEBUG)

    app.run(debug=True,port=5000,ssl_context=('Keys/cert.pem','Keys/key.pem'))
