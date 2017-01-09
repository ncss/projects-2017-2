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

def user_get_login(response):
    template = get_template('login.html')
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')
    if username.strip() != '' and password.strip() != '':
        # TODO: Add Database Check and redirect page
        response.write(username)
    else:
        response.write('You messed up')


def user_get_register(response):
    template = get_template('register.html')
    response.write(template)


def user_post_register(response):
    username = response.get_field('username')
    password = response.get_field('password')
    if username.strip() != '' and password.strip() != '':
        # TODO: Add Database Check and redirect page
        response.write(username + ' registered!')
    else:
        response.write('You messed up')


server = Server()
server.register("/", index)
server.register('/account', account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register', user_get_register, post=user_post_register)
server.run()
