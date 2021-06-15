from flask import Flask
from flask_restful import Api, Resource
from ApiMode import ApiSetting
from .ISS import getStatesOfShuttles, launchAShuttleFromEarth

class System(Resource):
    def get(self):
        return getStatesOfShuttles(), 201

    def post(self):
        launchAShuttleFromEarth()
        return {}, 201

class Iss(Resource):
    def get(self):
        raise Exception("todo - convert to json string")
        return getStatesOfShuttles(), 201

    def post(self):
        launchAShuttleFromEarth()
        return {}, 201

if ApiSetting.serverMode:
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(System, "/system/")
    app.run(debug=True,port=5000)