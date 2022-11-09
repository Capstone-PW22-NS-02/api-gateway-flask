from flask import request, abort
from device_detector import DeviceDetector


def token_required(ip_token_map):
    def decorator(api_caller):
        def wrapper(*args, **kwargs):

            ip = request.remote_addr
            # ip  = request.environ["HTTP_X_FORWARDED_FOR"]
            # user_agent  = request.headers['User-Agent']
            # device = DeviceDetector(user_agent).parse()
            # print(device.is_bot())  
            # print(device.os_name())   
            # print(device.os_version())
            # print(device.engine())
            # print(device.device_brand())
            # print(device.device_model())       
            # print(device.device_type())

            # print("IP : ", ip)
            # print("User-Agent : ", user_agent)


            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                print("Token : ",token)
            
            if not token:
                print("Map : ",ip_token_map)
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            if token in ip_token_map and ip_token_map[token] != ip:
                print("Map : ",ip_token_map)
                return {
                    "message": "This is an attempt for XSS attack",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            elif token not in ip_token_map:
                ip_token_map[token] = ip
                print("Map : ",ip_token_map)

            return api_caller(*args, **kwargs)

        wrapper.__name__ = api_caller.__name__
        return wrapper
    return decorator
