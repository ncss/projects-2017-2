from tornado.ncss import Server

FORM = '''
<!DOCTYPE html>
<html>
<head>
generic text
</head>
<body>
<form method="get">
Enter your name <input type="text" name="name"/>
<input type="submit"/>
</form>
</body>
</html>
'''

RESULT = '''
<!DOCTYPE html>
<html>
<head>
generic text
</head>
<body>
<h1>Hello {person}</h1>
</body>
</html>
'''


def test_get(response):
    name = response.get_field("name")
    if name is not None:
        response.write(RESULT.format(person=name))
    else:
        response.write(FORM)


server = Server()
server.register("/", test_get)
server.run()
