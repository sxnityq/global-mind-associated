import re 


class EmailValidator:

    pattern = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    
    def __init__(self):
        pass

    @classmethod
    def validate_email(cls, string: str):
        return re.match(pattern=cls.pattern,string=string) is not None
    