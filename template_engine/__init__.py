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

    def parse(self):
        node = self._parse_group()
        if not self.is_finished():
            raise Exception('Extra content found at end of input!')
        return node

    def _parse_group(self):
        nodes = []
        while self.peek() is not None:
            nodes.append(self._parse_node())
        return GroupNode(nodes)

    def _parse_node(self):
        if self.try_consume("{{"):
            return self._parse_python()
        else:
            return self._parse_text()

    def _parse_text(self):
        content = ""
        while self.peek() != "{" and self.peek() is not None:
            content += self.peek()
            self.next()
        return TextNode(content)

    def _parse_python(self):
        content = ""
        while not self.try_consume("}}"):
            if self.is_finished():
                raise TemplateError
            content += self.peek()
            self.next()
        return PythonNode(content)


class TemplateError(Exception):
    pass
