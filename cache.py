import time
import structures
from css_html_js_minify import html_minify, js_minify, css_minify
from rjsmin import jsmin

class Cache():
    def __init__(self, settings):
        self.cached = {}
        self.settings = settings
    def getFile(self, path):
        if (path in self.cached):
            # TODO: Check if cache has expired
            return self.cached[path]["data"]
        else:
            f = open(self.settings.get("webdir") + path, "r")
            data = f.read()
            f.close()

            if (self.settings.get("minify")):
                extension = path.split(".")[len(path.split(".")) - 1]
                if (extension in structures.FileTypes.html.value):
                    data = html_minify(data)
                elif (extension in structures.FileTypes.js.value):
                    data = jsmin(data)
                elif (extension in structures.FileTypes.css.value):
                    data = css_minify(data)
                

            
            # TODO: Check if path is in don't cache list

            self.cached[path] = {
                "data": data,
                "exp": 100000,
                "date": time.time()
            }

            return data