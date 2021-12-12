"""
Simple Go Winner Prediction API
"""

import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src", "models"))

from flask import Flask, jsonify
from PIL import Image
from flask_restful import Resource, Api, reqparse
from predict import Classifier  # :(
import requests
import numpy as np
import cv2


app = Flask(__name__)
api = Api(app)
ALLOWED_EXTENSIONS = {"png"}

parser = reqparse.RequestParser()
parser.add_argument("url", required=True, help="URL to the png image of your Go game")


class GoWinnerPredictor(Resource):
    def get(self):

        args = parser.parse_args()

        if args["url"].split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
            return jsonify(error="Images must be in .png format")

        try:
            responese = requests.get(args["url"], timeout=3)
            responese.raise_for_status()
        except:
            return jsonify(error="Error with connection to image url.")

        img = np.array(bytearray(responese.content), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        img = Image.fromarray(img).convert("RGB")

        return jsonify(url=args["url"], prediction=Classifier().predict(img))


api.add_resource(GoWinnerPredictor, "/")

if __name__ == "__main__":
    app.run(debug=True)
