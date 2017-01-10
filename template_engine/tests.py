import template_engine


def throws(template, context, message=None):
    try:
        template_engine.render(template, context)
    except template_engine.TemplateError as e:
        if message is not None:
            return str(e) == message
        return True
    else:
        return False

assert template_engine.render("foobar", {}) == "foobar"

assert template_engine.render("hello {{ name }}", {"name": "person"}) == "hello person"

assert template_engine.render("hello {{name}}", {"name": "person"}) == "hello person"

assert throws("hello {{name", {"name": "person"}), \
    'Expected TemplateError for unclosed python expression.'

assert template_engine.render("hello {{3+4}}", {}) == "hello 7"

assert template_engine.render("hello {{3+a}}", {'a': 4}) == "hello 7"

assert throws("hello {{a+b}}",
              {'a': 4},
              "the expression a+b failed with exception NameError: name 'b' is not defined"),\
    'Expected TemplateError for variable not in context'

assert template_engine.render("{% include 'helloworld.txt' %}", {}) == "hello world"

assert template_engine.render("{% include 'fortytwo.txt' %}", {}) == "54"

assert template_engine.render_file('helloworld.txt', {}) == "hello world"

assert template_engine.render_file('fortytwo.txt', {}) == "54"

assert template_engine.render('{{ value }}', {'value': '<html>'}) == "&lt;html&gt;"

assert template_engine.render('{{ value }}', {'value': template_engine.GroupNode}) == \
       '&lt;class &#x27;template_engine.GroupNode&#x27;&gt;'

assert template_engine.render('{% if True %}this{% endif %} and/or this', {}) == 'this and/or this'

assert template_engine.render('{% if value %}this{% endif %} and/or this', {'value': None}) == ' and/or this'

assert throws('{% if value %}failure', {}), 'if with no endif should fail'

assert throws('failure{% endif %}', {}), 'endif without matching if should fail'
