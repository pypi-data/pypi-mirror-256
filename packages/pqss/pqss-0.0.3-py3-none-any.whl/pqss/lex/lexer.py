from .token import Token, TokenType, lookup_keyword, is_color, is_property
from .utils import is_digit, is_letter, is_white_space
from .exceptions import TokenUnKnownException


class Lexer:
    """Lexer of PQSS"""
    def __init__(self, pqss_code: str):
        """
        :param pqss_code:  PQSS code
        """
        self.src_code: str = pqss_code

        self.cur_pos: int = 0   # 跟随者 to peek_pos
        self.peek_pos: int = 0  # 读取PQSS
        self.cur_char = None
        self.peek_char = None

        self.read_char()

    def read_char(self) -> str:
        """read a char and preview one char"""
        if self.peek_pos >= len(self.src_code):  # 到达文本末尾，全部读作EOF
            self.cur_char = 0
        else:
            # 更新状态
            self.cur_char = self.src_code[self.peek_pos]
            self.cur_pos = self.peek_pos
            self.peek_pos += 1
            if not self.peek_pos >= len(self.src_code):  # 到达文本末尾，字符不需要再改变了， 一律EOF
                self.peek_char = self.src_code[self.peek_pos]

        return self.cur_char

    # ':+(){}'
    def next_token(self) -> Token:
        """parse a lexeme to Token"""
        self.skip_white_space()  # TODO 优化一下跳过空的逻辑
        self.skip_comment()
        self.skip_white_space()

        lexeme = self.cur_char
        tok = None

        if lexeme == 0:
            tok = Token(TokenType.EOF, lexeme)

        elif lexeme == ':':
            tok = Token(TokenType.ASSIGN, lexeme)
        elif lexeme == '(':
            tok = Token(TokenType.LEFT_PAREN, lexeme)
        elif lexeme == ')':
            tok = Token(TokenType.RIGHT_PAREN, lexeme)
        elif lexeme == '{':
            tok = Token(TokenType.LEFT_BRACE, lexeme)
        elif lexeme == '}':
            tok = Token(TokenType.RIGHT_BRACE, lexeme)
        elif lexeme == ';':
            tok = Token(TokenType.SEMICOLON, lexeme)
        elif lexeme == ',':
            tok = Token(TokenType.COMMA, lexeme)

        elif lexeme == '+':
            tok = Token(TokenType.PLUS, lexeme)
        elif lexeme == '-':
            tok = Token(TokenType.SUB, lexeme)
        elif lexeme == '*':
            tok = Token(TokenType.MUL, lexeme)
        elif lexeme == '/':
            tok = Token(TokenType.DIV, lexeme)
        elif lexeme == '>':
            tok = Token(TokenType.GT, lexeme)
        elif lexeme == '<':
            tok = Token(TokenType.LT, lexeme)
        elif lexeme == '=':
            lexeme = '=='
            self.read_char()
            tok = Token(TokenType.EQ, lexeme)

        elif lexeme == '"' or lexeme == "'":
            pass  # 字符串 目前不接受插值

        elif lexeme == '&':
            tok = Token(TokenType.PARENT_REFERENCE, lexeme)
        elif lexeme == '$':
            lexeme = self.read_identifier()
            tok = Token(TokenType.IDENTIFIER, lexeme)
        elif lexeme == '!' or lexeme == '@':
            if self.peek_char == '=':
                lexeme = '!='
                self.read_char()
                tok = Token(TokenType.EQ, lexeme)
            else:
                tok = self.read_keyword()
        elif lexeme == '.':
            lexeme = self.read_ID_selector()
            tok = Token(TokenType.TYPE_SELECTOR, lexeme)
        elif lexeme == '#':
            lexeme = self.read_ID_selector()
            tok = Token(TokenType.ID_SELECTOR, lexeme)
        elif lexeme == '>':
            tok = Token(TokenType.CHILDREN_SELECTOR, lexeme)

        elif is_digit(lexeme):
            lexeme = self.read_number()
            tok = Token(TokenType.NUMBER, lexeme)

        elif lexeme == '%':
            raise NotImplementedError()

        elif is_letter(lexeme):
            if is_color(lexeme):
                raise NotImplementedError()
            elif self.is_property():
                lexeme = self.read_property()
                tok = Token(TokenType.PROPERTY, lexeme)
            elif self.is_keyword():
                tok = self.read_keyword()
            elif self.is_mixin_name():
                lexeme = self.read_identifier()
                tok = Token(TokenType.IDENTIFIER, lexeme)
            else:
                tok = self.read_selector()
        else:
            raise TokenUnKnownException(f'Token {lexeme} does unknown!!!')

        self.read_char()
        return tok

    def read_identifier(self):
        """read a valid identifier"""
        pos = self.cur_pos
        while is_letter(self.peek_char):
            self.read_char()
        return self.src_code[pos:self.peek_pos]

    def read_number(self):
        """read a valid number"""
        pos = self.cur_pos
        while is_digit(self.peek_char):  # int
            self.read_char()

        if self.peek_char == '.':  # float
            while is_digit(self.peek_char):
                self.read_char()
        return self.src_code[pos:self.peek_pos]

    def is_keyword(self) -> bool:
        """check the next word is a valid token for PQSS"""
        pos = self.cur_pos

        while is_letter(self.peek_char):
            self.read_char()
        lexeme = self.src_code[pos: self.cur_pos]

        # restore
        self.cur_pos = pos
        self.cur_char = self.src_code[self.cur_pos]
        self.peek_pos = pos + 1
        self.peek_char = self.src_code[self.peek_pos]

        if lookup_keyword(lexeme):
            return True
        return False

    def read_keyword(self):
        """read a keyword to Token"""
        pos = self.cur_pos

        while is_letter(self.peek_char):
            self.read_char()
        lexeme = self.src_code[pos:self.peek_pos]

        token_type = lookup_keyword(lexeme)
        if token_type is None:
            raise TokenUnKnownException(f'Token {lexeme} does not a valid keyword!!!')
        return Token(token_type, lexeme)

    def read_selector(self):
        """read the non-prefix selector"""
        pos = self.cur_pos
        token_type = None
        while is_letter(self.read_char()):
            pass

        # 属性选择器
        if self.cur_char == '[':
            while self.cur_char != ']':
                self.read_char()
            self.read_char()  # 读掉 ]
            token_type = TokenType.PROPERTY_SELECTOR
        elif self.cur_char == ':':
            if self.read_char() == ':':
                token_type = TokenType.SUBWIDGET_SELECTOR
            else:
                token_type = TokenType.PRODO_SELECTOR
            while is_letter(self.read_char()):
                pass
        else:
            token_type = TokenType.CLASS_SELECTOR
        return Token(token_type, self.src_code[pos:self.cur_pos])

    def read_ID_selector(self):
        """read the selector begin with #"""
        pos = self.cur_pos
        self.read_char()
        while is_letter(self.peek_char):
            self.read_char()
        return self.src_code[pos:self.cur_pos + 1]

    def is_property(self) -> bool:
        """check if the next word is property of QSS"""
        pos = self.cur_pos
        while is_letter(self.read_char()):
            pass
        lexeme = self.src_code[pos: self.cur_pos]
        self.cur_pos = pos
        self.cur_char = self.src_code[self.cur_pos]
        self.peek_pos = pos + 1
        self.peek_char = self.src_code[self.peek_pos]

        if is_property(lexeme):
            return True
        return False

    def read_property(self) -> str:
        """read the next properties and return the lexeme"""
        pos = self.cur_pos
        while is_letter(self.peek_char):
            self.read_char()
        lexeme = self.src_code[pos: self.peek_pos]
        if is_property(lexeme):
            return lexeme
        self.cur_pos = pos
        self.cur_char = self.src_code[pos]

    def is_mixin_name(self):
        """check if the next identifier belongs to a mixin"""
        i = 0
        while is_letter(self.src_code[self.cur_pos + i]):
            i += 1
        while is_white_space(self.src_code[self.cur_pos + i]):
            i += 1
        ch = self.src_code[self.cur_pos + i]
        return ch == '('

    def skip_white_space(self):
        """skip all the next black chars"""
        while is_white_space(self.cur_char):
            self.read_char()

    def skip_comment(self):
        """skip comments, // or /**/"""
        if self.cur_char == '/':
            if self.peek_char == '/':
                while self.cur_char != '\n':
                    self.read_char()
                self.read_char()  # skip \n
            elif self.peek_char == '*':
                stack = 1
                while stack != 0:
                    self.read_char()
                    if self.cur_char == '/' and self.peek_char == '*':
                        stack += 1
                    elif self.cur_char == '*' and self.peek_char == '/':
                        stack -= 1
                # skip */
                self.read_char()
                self.read_char()
