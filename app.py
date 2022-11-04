
from flask import Flask, request, flash, redirect, url_for, jsonify
from auth_middleware import token_required
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__, template_folder='.')
# app.secret_key = 'thisisjustarandomstring'
CORS(app)

ip_token_map = {}

@app.route('/inventory', methods=['POST', 'GET'])
@token_required(ip_token_map)
def index():
    if(request.method == 'GET'):
        
        # data = requests.get("http://inventory-service:8001/getProducts")
        data = requests.get("https://inventory-service-capstone.herokuapp.com/getProducts")
        data = data.json()
        return data



if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080,
        host="0.0.0.0"
    )
