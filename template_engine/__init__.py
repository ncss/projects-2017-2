def render(template, context):
    parser = Parser(template)
    node = parser.parse()
    return node.eval(context)


class PythonNode:
    def __init__(self, content):
        self.content = content

    def eval(self, context):
        try:
            return str(eval(self.content.strip(), {}, context))
        except Exception as e:
            raise TemplateError(
                'the expression {} failed with exception {}: {}'.format(
                    self.content,
                    type(e).__name__,
                    str(e)
                )
            )


class TextNode:
    def __init__(self, content):
        self.content = content

    def eval(self, context):
        return self.content


class GroupNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def eval(self, context):
        content = ""
        for node in self.nodes:
            content += node.eval(context)
        return content


class IncludeNode:
    def __init__(self, filename):
        self.filename = filename

    def eval(self, context):

        with open(self.filename) as f:
            file_content = f.read()
        return render(file_content, context)



class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._length = len(tokens)
        self._upto = 0

    def is_finished(self):
        return self._upto == self._length

    def peek(self, length=1):
        return None if self.is_finished() else self._tokens[self._upto:self._upto+length]

    def next(self):
        if not self.is_finished():
            self._upto += 1

    def try_consume(self, token):
        upcoming = self.peek(len(token))
        if upcoming == token:
            for _ in token:
                self.next()
            return True
        else:
            return False

    def _consume_whitespace(self):
        while self.peek() == ' ':
            self.next()

    def parse(self):
        node = self._parse_group()
        if not self.is_finished():
            raise TemplateError('Extra content found at end of input!')
        return node

    def _parse_group(self):
        nodes = []
        while self.peek() is not None:
            nodes.append(self._parse_node())
        return GroupNode(nodes)

    def _parse_node(self):
        if self.try_consume("{{"):
            return self._parse_python()
        elif self.try_consume("{%"):
            return self._parse_tag()
        else:
            return self._parse_text()

    def _parse_tag(self):
        self._consume_whitespace()
        if self.try_consume('include'):
            return self._parse_include()
        else:
            raise TemplateError('unknown tag')

    def _parse_include(self):
        self._consume_whitespace()
        if not self.try_consume('\''):
            raise TemplateError('expected \' after include')
        filename = self._read_to('\'', 'include')
        self._consume_whitespace()
        if not self.try_consume("%}"):
            raise TemplateError('expected %} after include tag')
        return IncludeNode(filename)

    def _parse_text(self):
        content = ""
        while self.peek(2) not in ("{{", "{%") and self.peek() is not None:
            content += self.peek()
            self.next()
        return TextNode(content)

    def _parse_python(self):
        return PythonNode(self._read_to("}}", "python"))

    def _read_to(self, token, name="tag"):
        result = ""
        while not self.try_consume(token):
            if self.is_finished():
                raise TemplateError('reached end of file while trying to parse {}, expected {}'.format(name, token))
            result += self.peek()
            self.next()
        return result

class TemplateError(Exception):
    pass
