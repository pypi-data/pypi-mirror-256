from webql.common.errors import QuerySyntaxError

from .character_utils import is_identifier_continue, is_identifier_start
from .source import Source
from .token import Token
from .token_kind import TokenKind

IGNORED_TOKENS = [TokenKind.NEWLINE]


class Lexer:
    def __init__(self, source: Source):
        """Initialize the lexer.

        Parameters:

        Source (Source): The source object."""
        start_of_file_token = Token(TokenKind.SOF, 0, 0, 1, 0)
        self.source = source
        """The previously focused non-ignored token."""
        self.last_token = start_of_file_token
        """The currently focused non-ignored token."""
        self.token = start_of_file_token
        """The (1-indexed) line containing the current token."""
        self.line = 1
        """The character offset at which the current line begins."""
        self.line_start = 0

    def __str__(self):
        return "Lexer"

    def advance(self) -> Token:
        """Advances the token stream to the next non-ignored token."""
        self.last_token = self.token
        self.token = self.lookahead()
        return self.token

    def lookahead(self) -> Token:
        """Looks ahead and returns the next non-ignored token, but does not change
        the state of Lexer."""
        token = self.token
        while True:
            if token.kind is TokenKind.EOF:
                break

            if token.next:
                token = token.next
            else:
                # Read the next token and form a link in the token linked-list.
                next_token = self._read_next_token(token.end)
                token.next = next_token
                next_token.prev = token
                token = next_token

            if token.kind not in IGNORED_TOKENS:
                break

        return token

    def _read_next_token(self, start: int) -> Token:
        """Gets the next token from the source starting at the given position.
        This skips over whitespace until it finds the next lexable token, then lexes
        punctuators immediately or calls the appropriate helper function for more
        complicated tokens.

        Parameters:

        start (int): The character offset at which to start reading the next token."""
        body = self.source.body
        body_length = len(body)

        position = start

        while position < body_length:
            code = ord(body[position])

            if code in (32, 9):  # space, tab
                position += 1
                continue
            if code == 13:  # carriage return \r
                if ord(body[position + 1]) == 10:
                    position += 2
                else:
                    position += 1
                self.line += 1
                self.line_start = position
                continue
            if code == 10:  # new line \n
                token_to_return = self._create_token(TokenKind.NEWLINE, start, position + 1)
                # Update line and line_start after creating the token
                self.line += 1
                self.line_start = position
                return token_to_return
            if code == 123:  # {
                return self._create_token(TokenKind.BRACE_L, start, position + 1)
            if code == 125:  # }
                return self._create_token(TokenKind.BRACE_R, start, position + 1)
            if code == 91:  # [
                return self._create_token(TokenKind.BRACKET_L, start, position + 1)
            if code == 93:  # ]
                return self._create_token(TokenKind.BRACKET_R, start, position + 1)

            if is_identifier_start(code):
                return self._read_name(position)

            raise QuerySyntaxError(
                unexpected_token=body[position],
                row=self.line,
                column=position - self.line_start + 1,
            )

        return self._create_token(TokenKind.EOF, body_length, body_length)

    def _create_token(self, kind: TokenKind, start: int, end: int, value: str = None) -> Token:
        """Create a token with line and column location information.

        Parameters:

        kind (TokenKind): The kind of the token.
        start (int): The character offset at which this Node begins.
        end (int): The character offset at which this Node ends.
        value (str): For non-punctuation tokens, represents the interpreted value of the token.

        Returns:

        Token: The created token."""
        line = self.line
        column = start - self.line_start + 1
        return Token(kind, start, end, line, column, value)

    def _read_name(self, start: int):
        position = start + 1
        body = self.source.body
        body_length = len(body)

        while position < body_length:
            code = ord(body[position])
            if not is_identifier_continue(code):
                break
            position += 1

        return self._create_token(TokenKind.IDENTIFIER, start, position, body[start:position])
