import base64

def gen_base64(login: str, password: str):
    encode_str = login + ":" + password
    return base64.b64encode(encode_str.encode()).decode()
