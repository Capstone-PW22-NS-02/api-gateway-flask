from flask import request, abort



def token_required(ip_token_map):
    def decorator(api_caller):
        def wrapper(*args, **kwargs):
            
            ip  = request.environ["REMOTE_ADDR"]
            # ip  = request.remote_addr
            print("IP : ", ip)
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                print(token)
            
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            if token in ip_token_map and ip_token_map[token] != ip:
                return {
                    "message": "This is an attempt for XSS attack",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            elif token not in ip_token_map:
                ip_token_map[token] = ip
                print("Map : ",ip_token_map)


            return api_caller(*args, **kwargs)

        return wrapper
    return decorator
