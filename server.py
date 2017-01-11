from tornado.ncss import Server
from template_engine.__init__ import render_file
import re


def index(response):
    if response.get_field('name'):
        template = render_file('templates/result.html', {'person': response.get_field('name')})
    else:
        template = render_file('templates/index.html', {})
    response.write(template)


def is_valid_username(username):
    if re.search('^[a-zA-Z0-9-.]+$', username):
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
        # TODO: Add Database Check and redirect page
        """
        try:
            user = Profiles.login(username, password)
        except ValueError as error:
            print(error)
        """
        response.redirect('/user/account/{}'.format(username))

    else:
        template = render_file('templates/login.html', {'message': 'Ha ha!\nIncorrect login details.'})
        response.write(template)


def user_get_register(response):
    template = render_file('templates/register.html', {})
    response.write(template)


def user_post_register(response):
    username = response.get_field('username')
    password = response.get_field('password')
    email = response.get_field('email')

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

def image_get_upload(response):
    template = render_file('templates/mock_upload.html', {})
    response.write(template)


def image_post_upload(response):
    f = response.get_file('upload')
    if f[0] == None:
        response.write('File not found.')
    else:
        template = render_file('templates/mock_upload.html', {})
        response.write(template)
        nf = open ('uploads/' + f[0],"wb+")
            # write to file
        nf.write(f[2])
        nf.close()


server = Server()
server.register("/", index)
server.register(r'/user/account/(\w+)', user_get_account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register', user_get_register, post=user_post_register)
server.register("/category/selection", category_get_selection, post=category_post_selection)
server.register("/upload", image_get_upload, post=image_post_upload)
server.run()
