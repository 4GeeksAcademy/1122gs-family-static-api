"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


John = {"id":1, "first_name": "John","last_name":jackson_family.last_name,"age": 33, "lucky_numbers": [7, 3, 22]}
Jane = {"id": 2, "first_name": "Jane","last_name":jackson_family.last_name, "age": 35, "lucky_numbers": [10, 14, 3]}
Jimmy = {"id": 3, "first_name": "Jimmy","last_name":jackson_family.last_name, "age": 5, "lucky_numbers": [1]}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)




# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member/<int:id>')
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404
# status_code: 200 if success. 400 if bad request (wrong info). 500 if the server encounters an error

@app.route('/member', methods=['POST'])
def add_new_member ():
    data = request.get_json()
    member = jackson_family.add_member(data)
    return jsonify(member),200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    data = jackson_family.delete_member(id)
    return jsonify(data), 200


@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
