# program → declaration | statement | block
# block → BEGIN statement END
# statement → declaration | if_statement | printf_statement | EOL
# if_statement → IF LPAREN expression RPAREN statement
# printf_statement → PRINTF LPAREN IDENT RPAREN SEMI
# declaration → INT (IDENT | declaration | COMMA)* SEMI
# expression → IDENT (RELOP IDENT)*
# Token → (INTEGER | LPAREN | RPAREN | COMMA | SEMI | EOL | INT | MAIN | PRINTF | BEGIN | END | IF | IDENT | RELOP)

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1

    def error(self):
        print(self.current_char)
        raise SyntaxError(f'Invalid character {self.current_char} at line {self.line}')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char == " ":
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char == " ":
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token('INTEGER', self.integer())

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            if self.current_char == '\n':
                self.advance()
                return Token('EOL', '\n')

            if self.current_char.isalpha():
                identifier = ''
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    identifier += self.current_char
                    self.advance()
                if identifier == 'int':
                    return Token('INT', 'int')
                elif identifier == 'main':
                    return Token('MAIN', 'main')
                elif identifier == 'printf':
                    return Token('PRINTF', 'printf')
                elif identifier == 'begin':
                    return Token('BEGIN', 'begin')
                elif identifier == 'end':
                    return Token('END', 'end')
                elif identifier == 'if':
                    return Token('IF', 'if')
                elif identifier == 'expr':
                    return Token('IDENT', 'expr')
                elif identifier == 'relop':
                    return Token('IDENT', 'relop')
                else:
                    return Token('IDENT', identifier)

            if self.current_char == '=':
                self.advance()
                return Token('RELOP', '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('RELOP', '!=')
                else:
                    self.error()

            if self.current_char == '<':
                self.advance()
                return Token('RELOP', '<')

            if self.current_char == '>':
                self.advance()
                return Token('RELOP', '>')

            if self.current_char == '=':
                self.advance()
                return Token('RELOP', '=')

            self.error()

        return Token('EOF')


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.line = 1

    def error(self):
        raise SyntaxError('Invalid syntax at line {}'.format(self.line))

    def eat(self, token_type):
        print("Eating token:", self.current_token.type, ", Value:", self.current_token.value)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def identifier_list(self):
        identifiers = [self.current_token.value]
        self.eat('IDENT')
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            identifiers.append(self.current_token.value)
            self.eat('IDENT')
        return identifiers

    def declaration(self):
        print("Declaration:")
        if(self.current_token.type=="INT"):
            self.eat("INT")

        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
        elif self.current_token.type == 'MAIN':
            self.eat('MAIN')
            self.eat('LPAREN')
            self.eat('RPAREN')
            self.eat("EOL")

        elif self.current_token.type == "IDENT":
            self.eat("IDENT")
            if self.current_token.type!="COMMA" and self.current_token.type!="SEMI":
                self.error()
            self.declaration()
        elif self.current_token.type == "COMMA":
            self.eat("COMMA")
            self.declaration()
        else:
            self.error()

    def if_statement(self):
        print("If Statement:")
        self.eat('IF')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')

        self.line += 1
        self.eat("EOL")
        self.block()

    def printf_statement(self):
        print("Printf Statement:")
        self.eat('PRINTF')
        self.eat('LPAREN')
        self.eat('IDENT')
        self.eat('RPAREN')
        self.eat('SEMI')

    def block(self):
        print("Block:")
        self.eat("BEGIN")
        while self.current_token.type != 'END':
            if self.current_token.type == "PRINTF":
                self.printf_statement()
            else:
                self.statement()
        self.eat("END")

    def statement(self):
        print("Statement:")
        if self.current_token.type == 'INT':
            self.declaration()
        elif self.current_token.type == 'EOL':
            self.line += 1
            self.eat('EOL')

        elif self.current_token.type == 'IF':
            self.if_statement()

        elif self.current_token.type == 'PRINTF':
            self.printf_statement()
        else:
            self.error()

    def expression(self):
        print("Expression:")
        self.eat('IDENT')
        while self.current_token.type == 'RELOP':
            self.eat('RELOP')
            self.eat('IDENT')

    def parse(self):
        print("Parsing started:")
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'INT':
                self.eat('INT')
                self.declaration()
            elif self.current_token.type == "EOL":
                self.line += 1
                self.eat("EOL")
            elif self.current_token.type == 'IF':
                self.if_statement()
            elif self.current_token.type == 'PRINTF':
                self.printf_statement()
            elif self.current_token.type == "BEGIN":
                self.block()
            elif self.current_token.type == 'EOF':
                self.eat("EOF")
            else:
                self.error()


text = """
int main()
begin
int n1, n, n3;
if( n1 > n2 )
begin
 printf(n1);
 end
 if ( n2 > n3 )
 begin
printf( n2);
 end
 if( n3 > n1 )
 begin
 printf( n3);
end
end"""
lexer = Lexer(text)
parser = Parser(lexer)

try:
    parser.parse()
    print("Parsing completed successfully.")
except SyntaxError as se:
    print("Syntax error during parsing:", se)
except Exception as e:
    print("Parsing failed due to an unexpected error:", e)