import structures

def parseRequest(text):
    
    lines = text.split("\n")

    # Check if request is valid, if not return None
    # TODO: Check if other lines are KEY: VALUE
    try:
        if (len(lines) < 1):
            return None
        if (lines[0].split(" ")[0].upper() not in structures.RequestTypes.list()): 
            return None
        if (len(lines[0].split(" ")) < 3):
            return None
    except:
        return None
    
    req = {}

    splitZero = lines[0].split(" ")
    req["type"] = splitZero[0].upper()
    req["dir"] = splitZero[1].lower()
    req["ver"] = splitZero[2].replace("\r", "")

    if (req["dir"][-1] == "/"):
        # TODO: Check if exists .html .htm .php ...
        req["dir"] += "index.html"

    for line in lines[1:]:
        splt = line.split(": ")
        if (len(splt) == 2):
            req[splt[0]] = splt[1].replace("\r", "")
    
    return req