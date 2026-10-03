import yaml
class ConfigLoader:

    _isinstance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._isinstance is None:
            cls._isinstance = super().__new__(cls)
        return cls._isinstance

    def __init__(self,path):
        if self._initialized:
            return
        self.path = path
        self.data = self._load_yaml()
        self._initialized = True

    def _load_yaml(self)->dict:
        with open(self.path,'r',encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_value(self,long_key:str):
        """
        接收属性式访问，like:a.b.c
        :param long_key:
        :return:
        """
        key_list = long_key.split('.')
        result = self.data
        for key in key_list:
            result = result.get(key)
        return result

if __name__ == '__main__':
    c = ConfigLoader('/data/POM.yaml')
    print(c.get_value('PageFileName.ClassName.PageElementName'))
