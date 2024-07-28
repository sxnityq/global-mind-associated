def basic_serializer(model: object):
    return model.__dict__.get("__data__")
