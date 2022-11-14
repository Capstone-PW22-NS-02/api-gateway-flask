from flask import request, abort
from device_detector import DeviceDetector
import httpagentparser

def token_required(ip_token_map):
    def decorator(api_caller):
        def wrapper(*args, **kwargs):

            # ip = request.remote_addr
            ip  = request.environ["HTTP_X_FORWARDED_FOR"]
            user_agent  = request.headers['User-Agent']
            device = DeviceDetector(user_agent).parse()
            # print(device.is_bot())  
            print("OS : ",device.os_name())  
            print("OS Version : ",device.os_version())
            print("Engine : ",device.engine())
            print("Device Brand : ",device.device_brand())
            print("Device Model : ",device.device_model())       
            print("Device Type : ",device.device_type())
            print("Browser : ",httpagentparser.simple_detect(user_agent)[1])
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

            if token in ip_token_map and ip_token_map[token] != ip:
                print("Line 6 => Map : ",ip_token_map)
                return {
                    "message": "This is an attempt for XSS attack",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            elif token not in ip_token_map:
                ip_token_map[token] = ip
                print("Line 7 => Map : ",ip_token_map)

            return api_caller(*args, **kwargs)

        wrapper.__name__ = api_caller.__name__
        return wrapper
    return decorator
