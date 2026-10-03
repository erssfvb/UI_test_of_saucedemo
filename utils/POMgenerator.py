import yaml

from utils.Loader.ConfigLoader import ConfigLoader


class POMgenerator:
    def __init__(self,path):
        self.template_path = path
        self.config_loader = ConfigLoader(self.template_path)

    def element_generator(self):
        pass

