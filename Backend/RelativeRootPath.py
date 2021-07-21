import pathlib

def getRelativeRootPath():
    return str(pathlib.Path(__file__).parent.absolute()).split("IssProject")[0] + "IssProject\\"