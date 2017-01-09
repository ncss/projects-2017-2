from tornado.ncss import Server
import os


def get_template(filename):
    with open(os.path.join('templates', filename)) as f:
        return f.read()



def index(response):
    if response.get_field('name'):
        template = get_template('result.html')
        template = template.format(person = response.get_field('name'))
    else:
        template = get_template('index.html')
    response.write(template)

#def account(name):
#    if name.get_field('name'):
#        template = get_template('account.html')
#        template = template.format(person = name.get_field('name'))

def account(response):
    template = get_template('account.html')
    response.write(template)

server = Server()
server.register("/", index)
server.register('/account', account)
server.run()
