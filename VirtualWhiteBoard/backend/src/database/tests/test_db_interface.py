
# Standard library
import unittest
import os

# VirtualWhiteBoard project
from database.db_interface import Interface, ActionState


class TestDbInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_interface = Interface()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("./data/data.db")

    def test_inserting_user(self):
        # 1
        # Creating new client
        state: ActionState = self.db_interface.create_user(
            "test_user", "test_pass", "EmailSometing")

        assert state == ActionState.SUCCESS, "Not able to create client"

        # 2 duplicating client
        state: ActionState = self.db_interface.create_user(
            "test_user", "test_pass", "EmailSometing")

        assert state == ActionState.FAILED, "Should not be able to create client"

    def test_authenticating_user(self):
        # 1
        # Authenticating user created above
        state: ActionState = self.db_interface.create_user(
            "test_user_2", "test_pass_2", "EmailSometing")
        assert state == ActionState.SUCCESS, "Not able to create client"
        state = self.db_interface.authenticate_user(
            "test_user_2", "test_pass_2")

        assert state == ActionState.SUCCESS, "Password was not authenticated"

        state = self.db_interface.authenticate_user(
            "test_user_2", "incorrect_password")

        assert state == ActionState.FAILED, "Password should have been rejected"

    def test_resetting_password(self):
        state: ActionState = self.db_interface.create_user(
            "test_user_4", "test_pass_4", "EmailSometing")
        assert state == ActionState.SUCCESS, "Not able to create client"

        state: ActionState = self.db_interface.reset_passsword(
            "test_user_4", "test_pass_4", "test_pass_5")

        assert state == ActionState.SUCCESS, "Not able to reset password"

        state: ActionState = self.db_interface.authenticate_user(
            "test_user_4", "test_pass_5")
        fail_state: ActionState = self.db_interface.authenticate_user(
            "test_user_4", "test_pass_4")

        assert state == ActionState.SUCCESS, "Password was not changed"
        assert fail_state == ActionState.FAILED, "The old password does still authenticate"
