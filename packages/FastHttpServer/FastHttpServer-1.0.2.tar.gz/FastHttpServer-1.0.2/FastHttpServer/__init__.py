import socket, json, threading
routes = {}

def view(path, methods=['GET']):
	def wrapper(func):
		routes[path] = {'func':func, 'methods':methods}
		return routes

	return wrapper

import json

def create_response(path, headers):
    if path in routes:
        if not headers['method'] in routes[path]['methods']:
            return 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nMethod Not Allowed'

        res = routes[path]['func'](headers)
        res_type = type(res).__name__

        # Check the type of response and construct the HTTP response accordingly
        if res_type == 'dict':
            response = f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
            response += 'Access-Control-Allow-Origin: *\r\n'  # Adding CORS header
            response += '\r\n'
            response += json.dumps(res)
            return response
        elif res_type == 'str':
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
            response += 'Access-Control-Allow-Origin: *\r\n'  # Adding CORS header
            response += '\r\n'
            response += res
            return response
    else:
        if '404' in routes:
            res = routes['404']['func'](headers)
            res_type = type(res).__name__
            if res_type == 'dict':
                response = f'HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\n'
                response += 'Access-Control-Allow-Origin: *\r\n'  # Adding CORS header
                response += '\r\n'
                response += json.dumps(res)
                return response
            elif res_type == 'str':
                response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n'
                response += 'Access-Control-Allow-Origin: *\r\n'  # Adding CORS header
                response += '\r\n'
                response += res
                return response
        else:
            return 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found'


def handle_connection(connection):
    req = connection.recv(1024).decode()
    key_val = req.split(None)    
    if len(key_val) < 2:
        return connection.close()    
    path = key_val[1].split('?')[0]
    url_params = key_val[1].split('?')[1] if '?' in key_val[1] else None    
    headers = {key.rstrip(':'): value for key, value in dict(zip(key_val[3:len(key_val)][0::2], key_val[3:len(key_val)][1::2])).items()}
    if url_params:
        url_params_dict = dict(kv.split('=') for kv in url_params.split('&'))
        headers.update(url_params_dict)
    headers['method'] = key_val[0]
    res = create_response(path, headers)
    connection.send(res.encode('utf-8'))
    connection.close()


def initServer(PORT=3000, ADDRESS='localhost'):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_socket.bind((ADDRESS, PORT))
	except:
		initServer(PORT + 1)
	server_socket.listen(128)
	print(f'Running on: http://localhost:{PORT}')

	while True:
		connection, address = server_socket.accept()
		threading.Thread(target=handle_connection, args=(connection,)).start()

class router:	
	route = view
	listen = initServer

def App(): return router