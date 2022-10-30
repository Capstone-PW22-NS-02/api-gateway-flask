from flask import request, abort



def token_required(ip_token_map):
    def decorator(api_caller):
        def wrapper(*args, **kwargs):
            
            ip  = request.environ["HTTP_X_FORWARDED_FOR"]
            # ip  = request.remote_addr
            # print("IP : ", ip)
            print("######################1")
            print(request.headers)
            print("######################2")
            print(request.data)
            print("######################3")
            print(list(request.args.listvalues()))
            print("######################4")
            print(request.endpoint)
            print("######################5")
            print(list(request.form.listvalues()))
            print("######################6")
            print(request.method)
            print("######################7")
            print(request.form)
            print("######################8")
            print(request.remote_addr)


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
