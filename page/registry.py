_REGISTER:dict[str,type] = {}

def registry(name:str):
    def deco(cls):
        _REGISTER[name] = cls
        return cls
    return deco

def get(name:str):
    return _REGISTER[name]

def all_pages()->dict[str,type]:
    return dict(_REGISTER)