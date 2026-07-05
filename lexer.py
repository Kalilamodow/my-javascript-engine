from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    KEYWD = "keyword"
    IDENT = "identifier"
    SEMI = "semi"

    LPAREN = "left paren"
    RPAREN = "right paren"
    LBRACE = "left brace"
    RBRACE = "right brace"
    LBRACK = "left bracket"
    RBRACK = "right bracket"

    ASSIGN = "assign"
    COMMA = "comma"
    COLON = "colon"

    DOT = "dot"
    PLUS = "plus"
    DASH = "minus"
    STAR = "times"
    SLASH = "slash"

    INC = "increment"
    DEC = "decrement"

    EQEQ = "double equals"
    NEQ = "not equals"
    GT = "greater"
    LT = "less"
    GREQ = "greater or equal"
    LEEQ = "less or equal"
    AND = "and"
    OR = "or"
    NOT = "not"

    STRING = "string"
    NUMBER = "number"

    ERROR = "syntax error"
    EOF = "done"


@dataclass
class Token:
    type: TokenType
    content: str


SPECIAL_CHARS = "!=.;()[]{}+-*/,:<>&|"
SPECIAL_CHAR_TOKENS = {
    "=": TokenType.ASSIGN,
    ".": TokenType.DOT,
    ";": TokenType.SEMI,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "==": TokenType.EQEQ,
    "+": TokenType.PLUS,
    "-": TokenType.DASH,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    ">": TokenType.GT,
    "<": TokenType.LT,
    ">=": TokenType.GREQ,
    "<=": TokenType.LEEQ,
    "&&": TokenType.AND,
    "||": TokenType.OR,
    "!": TokenType.NOT,
    "++": TokenType.INC,
    "--": TokenType.DEC,
}

SPECIAL_CHAR_TOKEN_LIST = list(SPECIAL_CHAR_TOKENS.keys())

KEYWORDS = ["if", "var", "while", "for", "function"]


class Lexer:
    code: str
    index: int

    def __init__(self, code: str) -> None:
        self.code = code
        self.index = 0

    def next(self) -> Token:
        self.next_whitespace()
        if self.index >= len(self.code):
            return Token(TokenType.EOF, "")

        character = self.code[self.index]

        if character in SPECIAL_CHARS:
            return self.next_special()

        if character.isalpha():
            return self.next_text()
        if character.isnumeric():
            return self.next_number()
        if character == '"':
            return self.next_string()

        raise Exception("invalid character " + character)

    def next_string(self) -> Token:
        text = ""
        prev_escape = False
        while True:
            self.index += 1
            if not self.check_index():
                return Token(TokenType.ERROR, "unterminated string literal")

            character = self.code[self.index]
            if prev_escape:
                text += character
                prev_escape = False
                continue

            if character == "\n":
                return Token(TokenType.ERROR, "unterminated string literal")

            if character == '"':
                self.index += 1
                break
            if character == "\\":
                prev_escape = True
                continue

            text += character

        return Token(TokenType.STRING, text)

    def next_number(self) -> Token:
        start_pos = self.index
        character = self.code[self.index]
        while character.isnumeric():
            self.index += 1
            if not self.check_index():
                break
            character = self.code[self.index]

        text = self.code[start_pos : self.index]
        return Token(TokenType.NUMBER, text)

    def next_text(self) -> Token:
        start_pos = self.index
        character = self.code[self.index]
        while character.isalnum() or character in "_$":
            self.index += 1
            if not self.check_index():
                break
            character = self.code[self.index]

        text = self.code[start_pos : self.index]

        return Token(
            TokenType.KEYWD if text in KEYWORDS else TokenType.IDENT,
            text,
        )

    def next_special(self) -> Token:
        text = ""

        while True:
            character = self.code[self.index]
            if character not in SPECIAL_CHARS:
                break
            text += character
            self.index += 1

            # if theres a defined token and theres no other defined token where it starts with that
            if ((token_type := SPECIAL_CHAR_TOKENS.get(text)) is not None) and (
                not any(
                    key != text and key.startswith(text)
                    for key in SPECIAL_CHAR_TOKEN_LIST
                )
            ):
                return Token(token_type, text)

            if not self.check_index():
                return Token(TokenType.EOF, "")

        # possible if for example = got cancelled
        if token := SPECIAL_CHAR_TOKENS[text]:
            return Token(token, text)

        return Token(TokenType.ERROR, "invalid operation")

    def next_whitespace(self):
        if not self.check_index():
            return
        character = self.code[self.index]
        while character.isspace():
            self.index += 1
            if not self.check_index():
                return
            character = self.code[self.index]

    def check_index(self):
        return self.index < len(self.code)


def lex(code: str) -> list[Token]:
    lexer = Lexer(code)
    tokens: list[Token] = []

    while True:
        token = lexer.next()
        if token.type is TokenType.EOF:
            break
        tokens.append(token)

    return tokens
