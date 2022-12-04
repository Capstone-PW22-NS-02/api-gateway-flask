from flask import request, abort
from device_detector import DeviceDetector
import httpagentparser
import urllib.parse
from flask_pymongo import pymongo

CONNECTION_STRING = 'mongodb+srv://suryamn:'+urllib.parse.quote_plus("qwerty@1234")+'@capstone.9nomawa.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('test')
hashmap_collection = pymongo.collection.Collection(db,'hashmap')

print("DB connection established")

def isXSS(user_map,user_details):

    print("Inside inXSS")
    count = 0
    if(user_map['os_name'] != user_details['os_name']):
        count += 1
    if(user_map['browser'] != user_details['browser']):
        count += 1
    if(user_map['ip'] != user_details['ip']):
        count += 1

    print("count : ",count)
    if(count >= 2):
        return True
    
    return False
        

def token_required():
    def decorator(api_caller):
        def wrapper(*args, **kwargs):

            print("Inside auth middleware")
            # ip = request.remote_addr
            ip  = request.environ["HTTP_X_FORWARDED_FOR"]
            user_agent  = request.headers['User-Agent']
            print("I'm in line 1")
            try:
                print("I'm in line 2")
                device = DeviceDetector(user_agent).parse()
            except Exception as e:
                print("I'm in line 3")
                print("Try catch")
                print(e)
            # print(device.is_bot()) 
            print("I'm in line 4")
            os_name = device.os_name()
            # os_version = device.os_version()
            # engine = device.engine()
            # device_brand = device.device_brand()
            # device_model = device.device_model()
            # device_type = device.device_type()
            print("I'm in line 5")
            browser = httpagentparser.simple_detect(user_agent)[1]
            print("I'm in line 6")
            user_details = {
                "os_name": os_name,
                "browser": browser,
                "ip" : ip
            } 

            print(user_details)
            print("OS : ", os_name)  
            # print("OS Version : ", os_version)
            # print("Engine : ",engine)
            # print("Device Brand : ", device_brand)
            # print("Device Model : ",device_model)       
            # print("Device Type : ",device_type)
            # print("Browser : ", browser)
            print("Line 1 => IP : ", ip)
            # print("Line 2 => User-Agent : ", user_agent)


            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                # print("Line 3 => Token : ",token)
                # print("Line 4 => Map : ",token_user_map)

            
            if not token:
                # print("Line 5 => Map : ",token_user_map)
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            token_user_map = hashmap_collection.find_one({"token":token},{'_id':0})
            print("token user map : ",token_user_map)

            if token_user_map and isXSS(token_user_map, user_details):
                print("Line 6 => Map : ",token_user_map)
                return {
                    "message": "This is an attempt for XSS attack",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            elif token_user_map is None:
                # token_user_map[token] = user_details
                new_token_map = {
                    "token" : token,
                    "browser": user_details["browser"],
                    "ip": user_details["ip"],
                    "os_name": user_details["os_name"],
                }
                hashmap_collection.insert_one(new_token_map)
                # print("Line 7 => Map : ",token_user_map)


            return api_caller(*args, **kwargs)

        wrapper.__name__ = api_caller.__name__
        return wrapper
    return decorator
