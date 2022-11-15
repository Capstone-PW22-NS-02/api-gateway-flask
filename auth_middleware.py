from flask import request, abort
from device_detector import DeviceDetector
import httpagentparser

def isXSS(ip_token_map,user_details):

    count = 0
    if(ip_token_map['os_name'] != user_details['os_name']):
        count += 1
    if(ip_token_map['browser'] != user_details['browser']):
        count += 1
    if(ip_token_map['ip'] != user_details['ip']):
        count += 1

    if(count >= 2):
        return True
    
    return False
        

def token_required(ip_token_map):
    def decorator(api_caller):
        def wrapper(*args, **kwargs):

            # ip = request.remote_addr
            ip  = request.environ["HTTP_X_FORWARDED_FOR"]
            user_agent  = request.headers['User-Agent']
            device = DeviceDetector(user_agent).parse()
            # print(device.is_bot()) 
            os_name = device.os_name()
            os_version = device.os_version()
            engine = device.engine()
            device_brand = device.device_brand()
            device_model = device.device_model()
            device_type = device.device_type()
            browser = httpagentparser.simple_detect(user_agent)[1]

            user_details = {
                "os_name": os_name,
                "browser": browser,
                "ip" : ip
            } 

            print("OS : ", os_name)  
            print("OS Version : ", os_version)
            print("Engine : ",engine)
            print("Device Brand : ", device_brand)
            print("Device Model : ",device_model)       
            print("Device Type : ",device_type)
            print("Browser : ", browser)
            print("Line 1 => IP : ", ip)
            # print("Line 2 => User-Agent : ", user_agent)


            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                print("Line 3 => Token : ",token)
                print("Line 4 => Map : ",ip_token_map)

            
            if not token:
                print("Line 5 => Map : ",ip_token_map)
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            if token in ip_token_map and isXSS(ip_token_map, user_details):
                print("Line 6 => Map : ",ip_token_map)
                return {
                    "message": "This is an attempt for XSS attack",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            elif token not in ip_token_map:
                ip_token_map[token] = user_details
                print("Line 7 => Map : ",ip_token_map)

            return api_caller(*args, **kwargs)

        wrapper.__name__ = api_caller.__name__
        return wrapper
    return decorator
