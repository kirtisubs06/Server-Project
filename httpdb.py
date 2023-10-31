import wsgiref.simple_server
import urllib.parse
import simpledb


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])

    db = simpledb.Simpledb('db.txt')

    if path == '/insert':
        name = params['key'][0]
        number = params['value'][0]
        db.insert(name, number)
        start_response('200 OK', headers)
        return ['INSERTED'.encode()]
    elif path == '/select':
        s = db.select_one(params['key'][0])
        start_response('200 OK', headers)
        if s:
            return [s.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/delete':
        name = params['key'][0]
        s = db.delete(name)
        start_response('200 OK', headers)
        if s:
            return ['DELETED'.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/update':
        name = params['key'][0]
        number = params['value'][0]
        s = db.update(name, number)
        start_response('200 OK', headers)
        if s:
            return ['UPDATED'.encode()]
        else:
            return ['NULL'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
