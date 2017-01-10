from tornado.ncss import Server
import os
from template_engine.__init__ import render_file
import re


# def get_template(filename):
#     with open(os.path.join('templates', filename)) as f:
#         return f.read()


def index(response):
    if response.get_field('name'):
        template = render_file('templates/result.html', {'person': response.get_field('name')})
    else:
        template = render_file('templates/index.html', {})
    response.write(template)


# def account(name):
#    if name.get_field('name'):
#        template = get_template('account.html')
#        template = template.format(person = name.get_field('name'))


def account(response, username):
    template = render_file('templates/account.html', {'name': username})
    response.write(template)


def is_valid_username(username):
    if re.search('^[a-zA-Z0-9-.]+$', username):
        return True
    else:
        return False


def user_get_login(response):
    template = render_file('templates/login.html', {'message':''})
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')

    if is_valid_username(username) and password.strip() != '':
        # TODO: Add Database Check and redirect page
        response.redirect('/account/{}'.format(username))
    else:
        template = render_file('templates/login.html', {'message': 'Ha ha!\nIncorrect login details.'})
        response.write(template)


def user_get_register(response):
    template = render_file('templates/register.html', {})
    response.write(template)


def user_post_register(response):
    username = response.get_field('username')
    password = response.get_field('password')

    if is_valid_username(username) and password.strip() != '':
        # TODO: Add Database Check and redirect page
        response.write(username + ' registered!')
    else:
        response.write('No password or username')


def category_get_selection(response):
    template = render_file('templates/category.html', {})
    response.write(template)


def category_post_selection(response):
    category = response.get_field('category')
    template = render_file('templates/category.html', {'category': category})
    response.write(template)


server = Server()
server.register("/", index)
server.register(r'/account/(\w+)', account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register/', user_get_register, post=user_post_register)
server.register("/category/selection", category_get_selection, post=category_post_selection)
server.run()
