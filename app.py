
from flask import Flask, request, flash, redirect, url_for, jsonify
from auth_middleware import token_required
from flask_cors import CORS,cross_origin
import requests

app = Flask(__name__, template_folder='.')
# app.secret_key = 'thisisjustarandomstring'
CORS(app)

ip_token_map = {}

@app.route('/inventory', methods=['GET'])
@cross_origin()
@token_required(ip_token_map)
def inventory():
        
    # data = requests.get("http://localhost:8001/getProducts")
    data = requests.get("https://inventory-service-capstone.herokuapp.com/getProducts")
    data = data.json()
    # print(data)
    return jsonify(data)

@app.route('/addProduct', methods=['POST'])
@cross_origin()
@token_required(ip_token_map)
def addProduct():        

    body = request.get_json()
    print(body)
    # data = requests.post("http://localhost:8001/addProduct",json=body)
    data = requests.post("https://inventory-service-capstone.herokuapp.com/addProduct", json=body)
    data = data.json()
    # data = {'msg':"Data added successfully"}
    return jsonify(data)



if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
