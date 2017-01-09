import template_engine

assert template_engine.render("foobar", {}) == "foobar"

assert template_engine.render("hello {{ name }}", {"name": "person"}) == "hello person"

assert template_engine.render("hello {{name}}", {"name": "person"}) == "hello person"
