from flask import Blueprint, jsonify, Response, make_response, request
# from app.project.datafilterops import Fitness_ops
from app.project.create_session import excel_to_json_file
# from app.project.movie_json import excel_to_json_file
mod_ppg = Blueprint("am", __name__, url_prefix='/am')


@mod_ppg.route("/health", methods=['GET'])
def health() -> Response:
    excel_to_json_file()
    return "succesfully convert excel file to json"

