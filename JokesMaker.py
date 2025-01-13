import random
import json

class JokesMaker:
    def __init__(self):
        self.jsonDict=None
        self.loadJson()

    def loadJson(self):
        with open ("jokes.json") as f:
            self.jsonDict=json.load(f)

    def getJoke(self,number):
        for id in self.jsonDict:
            if id == str(number):
                return str(self.jsonDict[id])
    def generateRandom(self):
        r1 = random.randint(1,len(self.jsonDict))
        return r1
    

