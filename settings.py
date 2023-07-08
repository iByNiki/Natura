class Settings():
    def __init__(self):
        self.data = {
            "host": "0.0.0.0",
            "port": 80,
            "webdir": "C:\\www",
            "minify": True
        }
    
    def get(self, key):
        if (key in self.data):
            return self.data[key]
        else:
            return None
    
# TODO: Make it load from file