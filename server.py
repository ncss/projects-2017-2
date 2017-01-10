from tornado.ncss import Server
import os
from template_engine.__init__ import render_file


def get_template(filename):
    with open(os.path.join('templates', filename)) as f:
        return f.read()


def index(response):
    if response.get_field('name'):
        template = render_file('templates/result.html', {'person': response.get_field('name')})
    else:
        template = render_file('index.html', None)
    response.write(template)

#def account(name):
#    if name.get_field('name'):
#        template = get_template('account.html')
#        template = template.format(person = name.get_field('name'))

def account(response):
    template = get_template('account.html').format(name = username)
    response.write(template)

def user_get_login(response):
    template = get_template('login.html')
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')
    if username.strip() != '' and password.strip() != '':
        # TODO: Add Database Check and redirect page
        template = get_template('account.html').format(name = username)
        response.write(template)
    else:
        template = get_template('login.html').format(message = 'Ha ha!\nIncorrect login details.')
        response.write(template)


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

def category_get_selection(response):
    template = get_template('category.html')
    response.write(template)

def category_post_selection(response):
    category = response.get_field('category')
    template = get_template('category.html').format(category=category)
    response.write(template)


server = Server()
server.register("/", index)
server.register('/account', account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register', user_get_register, post=user_post_register)
server.register("/category/selection", category_get_selection, post=category_post_selection)
server.run()
