from databases import Profiles
from databases import Database
from tornado.ncss import Server
from template_engine.__init__ import render_file
from databases import OriginalPost
import re

db = Database('databases/data.db')

def get_loggedin(response):
    loggedin = response.get_secure_cookie('username')
    if loggedin:
        return loggedin.decode('UTF8')

def index(response):
    template = render_file('templates/index.html', {"login": get_loggedin(response)})
    response.write(template)

def is_valid_email(email):
    LOCAL_REG = '^[\w\+\-\.]+'
    DOMAIN_REG = '[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)*'
    if re.search(LOCAL_REG + '@' + DOMAIN_REG, email) is not None:
        return email

def is_valid_username(username):
    if re.search('^[a-zA-Z0-9.-]+$', username):
        return True
    else:
        return False

def user_get_account(response, username):
    loggedin = get_loggedin(response)
    if username == loggedin:
        template = render_file('templates/account.html', {'login': loggedin})
        response.write(template)
    else:
        response.redirect('/user/login')

def confirm_login_redirect(response, username, password):
    try:
        Profiles.login(db, username, password)
        response.set_secure_cookie('username', username)
        response.redirect('/')
    except ValueError as error:
        template = render_file('templates/login.html', {'message': error,
                                                        'login': get_loggedin(response),
                                                        'username': username})
        response.write(template)

def user_get_login(response):
    template = render_file('templates/login.html', {'message': '',
                                                    'login': get_loggedin(response),
                                                    'username': ''})
    response.write(template)


def user_post_login(response):
    username = response.get_field('username')
    password = response.get_field('password')

    if is_valid_username(username) and password.strip() != '':
        confirm_login_redirect(response, username, password)
    else:
        template = render_file('templates/login.html', {'message': 'Incorrect login details.',
                                                        'login': get_loggedin(response),
                                                         'username': username})
        response.write(template)


def user_get_register(response):
    username = response.get_field('username')
    email = response.get_field('email')

    template = render_file('templates/register.html', {'message': '',
                                                       'login': get_loggedin(response),
                                                       'username': '',
                                                       'email': ''})
    response.write(template)


def user_post_register(response):
    username = response.get_field('username')
    password = response.get_field('password')
    email = response.get_field('email')

    if is_valid_username(username) and is_valid_email(email) and password.strip() != '':
        try:
            Profiles.register(db, username, password, email)
            confirm_login_redirect(response, username, password)
        except ValueError as error:
            template = render_file('templates/register.html', {'message': error, 'login': get_loggedin(response)})
            response.write(template)
    else:
        template = render_file('templates/register.html', {'message': 'Invalid username or password. Please try again.',
                                                           'login': get_loggedin(response),
                                                           'username': username,
                                                           'email': email})
        response.write(template)

def user_get_logout(response):
    response.clear_cookie('username')
    response.redirect("/")

def category_get_selection(response):
    template = render_file('templates/category.html', {'login': get_loggedin(response)})
    response.write(template)


def category_post_selection(response):
    category = response.get_field('category')
    template = render_file('templates/category.html', {'category': category, 'login': get_loggedin(response)})
    response.write(template)

#TODO images
def see_photo_and_response(response, image_ids):
    template = render_file('templates/sketchresponse.html', {'login': get_loggedin(response)})
    response.write(template)

def image_get_upload(response):
    username = response.get_secure_cookie('username')
    template = render_file('templates/uploadphotos.html', {'message': '', 'login':username})
    response.write(template)

def image_post_upload(response):
    f = response.get_file('upload')
    file_extension = str(f[0]).split('.')[-1]
    image = f[2]  # Bytes
    content = response.get_field('content')
    username = response.get_secure_cookie('username')
    if not username:
        template = render_file('templates/uploadphotos.html', {'message': 'You need to Log in first', 'login':username})
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
server.register('/photo/view', see_photo_and_response)
server.register("/photo/upload", image_get_upload, post=image_post_upload)

server.run()
