from tornado.ncss import Server

def index(response):
    response.write("Hello World")

server = Server()
server.register("/",index)
server.run()