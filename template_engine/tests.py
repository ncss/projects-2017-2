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