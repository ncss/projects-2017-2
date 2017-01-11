from databases import Profiles
from databases import Database
from tornado.ncss import Server
from template_engine.__init__ import render_file
from databases import OriginalPost
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
    loggedin = response.get_secure_cookie('username')
    print(username, loggedin)
    if username.encode('UTF8') == loggedin:
        template = render_file('templates/account.html', {'name': username})
        response.write(template)
    else:
        response.redirect('/user/login')

def confirm_login_redirect(response, username, password):
    try:
        Profiles.login(db, username, password)
        response.set_secure_cookie('username', username)
        response.redirect('/')
        print('Logging in as ' + username)
    except ValueError as error:
        print(error)
        template = render_file('templates/login.html', {'message': error})
        response.write(template)

def user_get_login(response):
    template = render_file('templates/login.html', {'message': ''})
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')

    if is_valid_username(username) and password.strip() != '':
        confirm_login_redirect(response, username, password)
    else:
        template = render_file('templates/login.html', {'message': 'Incorrect login details.'})
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
            confirm_login_redirect(response, username, password)
        except ValueError as error:
            template = render_file('templates/register.html', {'message': error})
            response.write(template)
    else:
        template = render_file('templates/register.html', {'message': 'Invalid Username or Password'})
        response.write(template)

def user_get_logout(response):
    response.clear_cookie('username')
    response.redirect("/")

def category_get_selection(response):
    template = render_file('templates/category.html', {})
    response.write(template)


def category_post_selection(response):
    category = response.get_field('category')
    template = render_file('templates/category.html', {'category': category})
    response.write(template)


def image_get_upload(response):
    username = response.get_secure_cookie('username')
    template = render_file('templates/uploadphotos.html', {'message': '', 'loged_in':username})
    response.write(template)


def image_post_upload(response):
    f = response.get_file('upload')
    file_extension = str(f[0]).split('.')[-1]
    image = f[2]  # Bytes
    content = response.get_field('content')
    username = response.get_secure_cookie('username')
    if not username:
        template = render_file('templates/uploadphotos.html', {'message': 'You need to Log in first6'})
        response.write(template)
    else:
        username = username.decode()
        post = OriginalPost.create(db, Profiles.from_user(db, username).id, content)
        print(post)
        path = "static/" + str(post.id) + "." + file_extension
        with open(path, "wb") as file:
            file.write(image)
        response.redirect("/")


server = Server()
server.register("/", index)
server.register(r'/user/account/(\w+)', user_get_account)
server.register('/user/login', user_get_login, post=user_post_login)
server.register('/user/register', user_get_register, post=user_post_register)
server.register('/user/logout' , user_get_logout)
server.register("/category/selection", category_get_selection, post=category_post_selection)
server.register("/photo/upload", image_get_upload, post=image_post_upload)
server.run()