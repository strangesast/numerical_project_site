
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, static_file

@route('/')
def hello_world():
    #return 'Hello from Bottle!'
    return static_file('index.html', root='/home/strangesast/mysite/')

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/home/strangesast/linear_algebra_project/')

application = default_app()
