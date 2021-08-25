
# Standard library

# This component
from api.login_api import Authentication, ResetPassword, Users
from api.white_board_api import ImageLinks, MotivationalText

# Third party library
from flask import Flask
from flask_restful import Api
import pandas as pd
import ast


def setup_api():
    app = Flask("VirtualWhiteBoard")
    api = Api(app)
    # User resources
    api.add_resource(Users, "/users")
    api.add_resource(Authentication, "/user/authentication")
    api.add_resource(ResetPassword, "/user/password_reset")

    # Whiteboard resources
    api.add_resource(MotivationalText, "/white_board/motivational_text")
    api.add_resource(ImageLinks, "/white_board/image_links")

    return app


def init_api():
    app = setup_api()

    app.run()
