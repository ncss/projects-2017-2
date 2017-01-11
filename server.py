from databases import Profiles
from databases import Database
from tornado.ncss import Server
from template_engine.__init__ import render_file
import re

db = Database('databases/data.db')

def index(response):
    if response.get_field('name'):
        template = render_file('templates/result.html', {'person': response.get_field('name')})
    else:
        template = render_file('templates/index.html', {})
    response.write(template)


def is_valid_username(username):
    if re.search('^[a-zA-Z0-9.-]+$', username):
        return True
    else:
        return False


def user_get_account(response, username):
    template = render_file('templates/account.html', {'name': username})
    response.write(template)


def user_get_login(response):
    template = render_file('templates/login.html', {'message': ''})
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')

    if is_valid_username(username) and password.strip() != '':
        try:
            Profiles.login(db, username, password)
            response.redirect('/user/account/{}'.format(username))
        except ValueError as error:
            print(error)
            template = render_file('templates/login.html', {'message': error})
            response.write(template)
    else:
        template = render_file('templates/login.html', {'message': 'Ha ha!\nIncorrect login details.'})
        response.write(template)


def user_get_register(response):
    template = render_file('templates/register.html', {'message':''})
    response.write(template)


def user_post_register(response):
    username = response.get_field('username')
    password = response.get_field('password')
    email = response.get_field('email')

    if is_valid_username(username) and password.strip() != '':
        try:
            Profiles.register(db, username, password, email)
            response.write(username + ' registered!')
        except ValueError as error:
            template = render_file('templates/register.html', {'message': error})
            response.write(template)
    else:
        template = render_file('templates/register.html', {'message': 'Invalid Username or Password'})
        response.write(template)


def category_get_selection(response):
    template = render_file('templates/category.html', {})
    response.write(template)


def category_post_selection(response):
    category = response.get_field('category')
    template = render_file('templates/category.html', {'category': category})
    response.write(template)


server = Server()
server.register("/", index)
server.register(r'/user/account/(\w+)', user_get_account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register', user_get_register, post=user_post_register)
server.register("/category/selection", category_get_selection, post=category_post_selection)
server.run()