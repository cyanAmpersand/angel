def loadToken(filename):
    f = open(filename,"r")
    token = f.read()
    f.close()
    return token