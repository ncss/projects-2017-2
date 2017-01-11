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


def assert_renders(template, context, expected):
    try:
        parser = template_engine.Parser(template)
        node = parser.parse()
        result = node.eval(context)
        if result != expected:
            print('template:', template)
            print('result:', result)
            print('expected:', expected)
            print('context:', context)
            print(repr(node))
            print()
    except Exception:
        print('template:', template)
        print('expected:', expected)
        print('context:', context)
        raise

assert_renders("foobar", {}, "foobar")

assert_renders("hello {{name}}", {"name": "person"}, "hello person")

assert_renders("hello {{ name }}", {"name": "person"}, "hello person")

assert throws("hello {{name", {"name": "person"}), \
    'Expected TemplateError for unclosed python expression.'

assert_renders("hello {{3+4}}", {}, "hello 7")

assert_renders("hello {{3+a}}", {'a': 4}, "hello 7")

assert throws("hello {{a+b}}",
              {'a': 4},
              "the expression a+b failed with exception NameError: name 'b' is not defined"),\
    'Expected TemplateError for variable not in context'

assert_renders("{% include 'helloworld.txt' %}", {}, "hello world")

assert_renders("{% include 'fortytwo.txt' %}", {}, "54")

assert template_engine.render_file('helloworld.txt', {}) == "hello world"

assert template_engine.render_file('fortytwo.txt', {}) == "54"

assert_renders('{{ value }}', {'value': '<html>'}, "&lt;html&gt;")

assert_renders(
    '{{ value }}',
    {'value': template_engine.GroupNode},
    '&lt;class &#x27;template_engine.GroupNode&#x27;&gt;'
)
assert_renders('{% if True %}this{% endif %} and/or this', {}, 'this and/or this')

assert_renders('{% if value %}this{% endif %} and/or this', {'value': None}, ' and/or this')

assert throws('{% if value %}failure', {}), 'if with no endif should fail'

assert throws('failure{% endif %}', {}), 'endif without matching if should fail'

assert throws('{% ifvalue %}this{% endif %} and/or this', {'value': None}),'no space after if should fail'

assert throws("{% include'helloworld.txt' %}", {}), 'no space after include should fail'

assert_renders('{% for a in b%}s:{{a}}:e{%endfor%}', {'b': [1, 2, 3]}, 's:1:es:2:es:3:e')

assert throws('{% fora in b%}s:{{a}}:e{%endfor%}', {'b': [1, 2, 3]}), 'no space after for should fail'

assert_renders('{% for a in b%}{{a}}{%endfor%}', {'b': (c for c in 'abc')}, 'abc')

assert_renders('{% for a in b%}{{a}}{% for c in d%}{{c}}{%endfor%}{%endfor%}', {'b': [1, 2], 'd': [3, 4]}, '134234')

assert_renders('{% for a in b%}{{a}}{% for a in b%}{{a}}{%endfor%}{%endfor%}', {'b': [1, 2]}, '112212')

assert_renders(
    '{% if True %}this{% if True %}that{% endif %}stuff{% endif %}things',
    {},
    'thisthatstuffthings'
)

assert_renders('{% if value %}this{% else %}that{% endif %} yay', {'value': False}, 'that yay')

assert_renders('abc {% if value %}this{% else %}that{% endif %} yay', {'value': True}, 'abc this yay')

assert throws('abc {% if value %}this{% else %} {%else%} that{% endif %} yay', {'value': True}),\
    'else outside of if should fail'

assert_renders(
    'this {% for a in b %} {{a}} {% empty %} that {% endfor %} and the other.',
    {"b": []},
    'this  that  and the other.'
)

assert throws('not in a for --> {% empty %}', {}), 'empty tag outside of for should fail'

assert_renders(
    'this {% for a in b %} {{a}} {% empty %} that {% endfor %} and the other.',
    {"b": [1, 2]},
    'this  1  2  and the other.'
)

assert_renders('{% safe value %}', {'value': '<html>'}, "<html>")

assert_renders('{%        safe value%}', {'value': '<html>'}, "<html>")

assert_renders(
    '{%safe value %}',
    {'value': template_engine.GroupNode},
    '<class \'template_engine.GroupNode\'>'
)

assert throws('{%safevalue%}', {'value': '<html>'}), 'no space after safe should fail'

assert_renders('{% comment %}asfgasdfasdfa{% endcomment %}', {}, '')

assert_renders('{%comment%}{% asdfasdfasdf %}{%endcomment         %}', {}, '')

assert_renders('start{%comment%}{% asdfasdfasdf %}{%endcomment%}end', {}, 'startend')

assert_renders('{%comment%}{% if True %}chicken{%endif%}{%endcomment%}', {}, '')

assert throws('{%comment%}{% if True %}chicken{%endcomment%}{%endif%}', {}), 'tags should be invalid inside comment'

assert throws('{% if True %}{%comment%}chicken{%endif%}{%endcomment%}', {}), 'tags should be invalid inside comment'

assert_renders(
    'this {% for a, b in c %} {{a}}:{{b}} {% empty %} that {% endfor %} and the other.',
    {"c": {1: "one", 2: "two"}.items()},
    'this  1:one  2:two  and the other.'
)

assert throws('{% for a, in b %} {{a}} {% endfor %}', {'b': [1, 2]}), 'comma followed only by in should fail'

assert throws('{% for a, b in c %} {{a}} {% endfor %}', {'c': [(1, 2, 3), (4, 5, 6)]}),\
    'incorrect number of tuples to unpack should fail'

assert_renders('{% for a in b %} {{a}} {% endfor %}', {'b': []}, '')