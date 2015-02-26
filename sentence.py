import pattern.en as pat

class Sentence:
    
    personDict = {'i':1, 'you':2, 'he':3, 'she':3, 'it':3, 'we':1, 'you':2, 'they':3}
    
    def conjugateVerbs(self, noun, verb, tags):
        person = 3
        
        if noun in personDict:
            person = personDict[noun]
        return pat.conjugate(verb, person=person)
        
    def processWord(self, word, tags):
        if len(tags) == 0:
            return word
        return "boop"
    
    def parse(self):
        self.parsed = []
        
        word = self.raw[0]
        tags = []
        for i in xrange(1, len(self.raw)):
            curr = self.raw[i]
            if curr[0][0] == '[':
                tags.append(curr[0])
            else:
                self.parsed.append(self.processWord(word, tags))
                word = curr
        
        self.parsed.append(self.processWord(word, tags))
    
    def __init__(self, obj=[]):
        self.raw = obj
        self.parse()
        
sen = Sentence([['Jason'], [','], ['to hold', 'to carry', 'to possess'], ['[PROG]'], ['[QUE]'], ['family', 'members of a family'], ['[POS]'], ['photograph', 'photo', 'movie'], ['[OBJ]']])

print sen.parsed