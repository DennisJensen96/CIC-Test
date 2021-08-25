# Standard library
from typing import List

# Virtual White board project components
from database.db_interface import WhiteBoardData

# Third party library
from flask_restful import Resource, reqparse


class MotivationalText(Resource):
    """[summary]
    Motivational text to put on the white board. No longer then 280 characters.
    """

    def __init__(self) -> None:
        self.db = WhiteBoardData()
        self.max_length = 280

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('text', required=True)

        args = parser.parse_args()
        text = args["text"]

        if len(text) > 280:
            return {"message": "The input text was too long"}, 403

        self.db.update_json({"motivational_text": text})
        return {"data": text}, 200

    def get(self):
        motivational_text = self.db.get_data()["motivational_text"]
        return {"data": motivational_text}, 200


class ImageLinks(Resource):
    """[summary]
    Handling image links for the white board.
    """

    def __init__(self) -> None:
        self.db = WhiteBoardData()

    def get(self):
        image_links = self.db.get_data()["image_links"]
        return {"data": image_links}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('image_link', required=True)
        args = parser.parse_args()
        image_link: str = args["image_link"]

        if "https" not in image_link or image_link == None:
            return {"message": "please provide valid image link with https."}, 403

        image_links = self.db.get_data()["image_links"]
        print(image_links)
        image_links.append(image_link)

        if not len(image_links) > 0:
            return {"message": "please provide valid image link with https."}, 403

        self.db.update_json({"image_links": image_links})

        return {"data": image_links}, 200

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('image_link', required=True)
        args = parser.parse_args()
        image_link: str = args["image_link"]

        image_links: List[str] = self.db.get_data()["image_links"]

        image_links.remove(image_link)
        self.db.update_json({"image_links": image_links})
        return {"data": image_links}, 200
