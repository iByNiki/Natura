import yaml

SETTINGS_FILE = "config.yml"

class Settings():
    def __init__(self):
        pass
    
    def get(self, key):
        if (key in self.data):
            return self.data[key]
        else:
            return None
        
    def load(self, file=SETTINGS_FILE):
        f = open(file, "r")

        try:
            self.data = yaml.safe_load(f)
        except yaml.YAMLError as err:
            print(err)
            self.data = None

        f.close()
    
# TODO: Make it load from file