import json
class DataLoader:
    def __init__(self,path):
        self.path = path
        self.data = self._load_data()

    def _load_data(self):
        with open(self.path,'r',encoding='utf-8') as f:
            return json.load(f)

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

