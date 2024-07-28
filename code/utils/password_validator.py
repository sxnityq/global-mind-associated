import re 


class PasswordValidator:

    pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
    
    def __init__(self):
        pass

    @classmethod
    def validate_password(cls, string: str):
        return re.match(pattern=cls.pattern, string=string) is not None