class TokenType:
    def __init__(self, type_name) -> None:
        self.type_name = type_name


class Token:
    def __init__(self, token_type, literal) -> None:
        self.token_type = token_type
        self.literal = literal
