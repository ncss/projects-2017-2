import html

def render_file(filename, context):
    with open(filename) as f:
        template = f.read()
    return render(template, context)


def render(template, context):
    parser = Parser(template)
    node = parser.parse()
    #print(repr(node))
    return node.eval(context)

def _evaluate_python(content, context):
    try:
        return eval(content, {}, context)
    except Exception as e:
        raise TemplateError(
            'the expression {} failed with exception {}: {}'.format(
                content,
                type(e).__name__,
                str(e)
            )
        )


class PythonNode:
    def __init__(self, content):
        self.content = content.strip()

    def __repr__(self):
        return 'PythonNode({!r})'.format(self.content)

    def eval(self, context):
        value = _evaluate_python(self.content, context)
        return html.escape(str(value))


class TextNode:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return 'TextNode({!r})'.format(self.content)

    def eval(self, context):
        return self.content


class GroupNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def __repr__(self):
        return 'GroupNode({})'.format(self.nodes)

    def eval(self, context):
        content = ""
        for node in self.nodes:
            content += node.eval(context)
        return content


class IncludeNode:
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return 'IncludeNode({!r})'.format(self.filename)

    def eval(self, context):
        return render_file(self.filename, context)


class IfNode:
    def __init__(self, expression, true_group, false_group):
        self.expression = expression
        self.true_group = true_group
        self.false_group = false_group

    def __repr__(self):
        return 'IfNode({!r}, {!r})'.format(self.expression, self.true_group, self.false_group)

    def eval(self, context):
        if _evaluate_python(self.expression, context):
            return self.true_group.eval(context)
        else:
            if self.false_group is not None:
                return self.false_group.eval(context)
            else:
                return ''


class ForNode:
    def __init__(self, item, sequence, for_group, empty_group):
        self.item = item
        self.sequence = sequence
        self.for_group = for_group
        self.empty_group = empty_group

    def __repr__(self):
        return 'ForNode({!r}, {!r}, {!r})'.format(self.item, self.sequence, self.for_group, self.empty_group)

    def eval(self, context):
        content = ""
        try:
            iterable = context[self.sequence]
        except KeyError:
            raise TemplateError('could not parse for tag, iterable {} not in context'.format(self.sequence))
        try:
            iter(iterable)
        except TypeError:
            raise TemplateError('{} is not iterable'.format(self.sequence))
        looped = False
        for element in iterable:
            looped = True
            current_context = context.copy()
            current_context[self.item] = element
            content += self.for_group.eval(current_context)
        if not looped:
            content += self.empty_group.eval(context)
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
        if token is None:
            return False
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

    def _parse_group(self, terminal_tag=None):
        nodes = []
        try:
            while self.peek() is not None:
                nodes.append(self._parse_node())
        except EndGroupException:
            if terminal_tag is None:
                raise TemplateError('unexpected end tag')
        else:
            if terminal_tag is not None:
                raise TemplateError('expected {}'.format(terminal_tag))
        return GroupNode(nodes)

    def _parse_else_or_empty_group(self, terminal_tag=None):
        """
        Returns two groups, one that is prior to the else or empty tag (if there one, otherwise it is the whole thing),
        and another, which is after the else or empty tag, unless there isn't one, in which case it is None.
        """
        nodes = []
        try:
            while self.peek() is not None:
                nodes.append(self._parse_node())
        except EndGroupException:
            first_group = GroupNode(nodes)
            second_group = None
        except (ElseException, EmptyException):
            first_group = GroupNode(nodes)
            second_group = self._parse_group(terminal_tag)
        else:
            raise TemplateError('expected {}'.format(terminal_tag))
        return first_group, second_group

    def _parse_node(self):
        if self.try_consume("{{"):
            return self._parse_python()
        elif self.try_consume("{%"):
            return self._parse_tag()
        else:
            return self._parse_text()

    def _parse_tag(self):
        self._consume_whitespace()
        if self.try_consume('include '):
            return self._parse_include()
        elif self.try_consume('if '):
            return self._parse_if()
        elif self.try_consume('endif '):
            self._parse_end()
        elif self.try_consume('for '):
            return self._parse_for()
        elif self.try_consume('endfor'):
            return self._parse_end()
        elif self.try_consume('else'):
            self._parse_else()
        elif self.try_consume('empty'):
            self._parse_empty()
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

    def _parse_if(self):
        self._consume_whitespace()
        expression = self._read_to("%}", "if").strip()
        true_group, false_group = self._parse_else_or_empty_group('endif')
        return IfNode(expression, true_group, false_group)

    def _parse_end(self):
        self._end_tag('end')
        raise EndGroupException('unexpected end tag')
        # its not really always unexpected

    def _parse_else(self):
        self._end_tag('else')
        raise ElseException('unexpected else tag')

    def _parse_empty(self):
        self._end_tag('empty')
        raise EmptyException('unexpected empty tag')

    def _end_tag(self, name):
        self._consume_whitespace()
        if not self.try_consume('%}'):
            raise TemplateError('expected \'%}\' at end of {} tag'.format(name))

    def _parse_for(self):
        self._consume_whitespace()
        item = self._read_to(' ', 'for')
        self._consume_whitespace()
        if not self.try_consume('in '):
            raise TemplateError('expected\'in \' after {}'.format(item))
        sequence = self._read_to("%}", "for").strip()
        for_group, empty_group = self._parse_else_or_empty_group('endfor')
        return ForNode(item, sequence, for_group, empty_group)

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


class EndGroupException(TemplateError):
    pass


class ElseException(TemplateError):
    pass


class EmptyException(TemplateError):
    pass