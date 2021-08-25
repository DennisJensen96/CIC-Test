
# Standard library

# This component
from api.login_api import Authentication, Users
from api.white_board_api import WhiteBoard

# Third party library
from flask import Flask
from flask_restful import Api
import pandas as pd
import ast


def init_api():
    app = Flask("VirtualWhiteBoard")
    api = Api(app)

    api.add_resource(Users, "/users")
    api.add_resource(Authentication, "/user/authentication")
    api.add_resource(WhiteBoard, "/white_board")

    app.run()
