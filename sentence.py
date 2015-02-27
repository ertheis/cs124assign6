import pattern.en as pat
import EnglishModel as em

class Sentence:
    
    personDict = {'I':'1', 'you':'2', 'he':'3', 'she':'3', 'it':'3', 'we':'1', 'you':'2', 'they':'3'}
    verbMod = ['[PROG]', '[PAST]']
    
    def noTags(self):
        tagsRemoved = []
        for word in self.parsed:
            tagsRemoved.append(word[0])
        
        return tagsRemoved
        
    def conjugateBe(self, noun, plural = False, past = False):
        person = '3'
        if noun in self.personDict:
            person = self.personDict[noun]
            
        if past:
            if plural:
                return "were"
            else:
                if person == '1':
                    return "was"
                elif person == '2':
                    return "were"
                else:
                    return "was"
        else:
            if plural:
                return "are"
            else:
                if person == '1':
                    return "am"
                elif person == '2':
                    return "are"
                else:
                    return "is"
    
    def initialPass(self):
        for i in xrange(len(self.parsed)):
            word = self.parsed[i]
            text = word[0]
            tags = word[1]
            
            if '[QUE]' in tags:
                self.que = True
                self.parsed.append([["?"], []])
                
            if '[WA]' in tags:
                self.subj = text[0]
                
            if '[POS]' in tags:
                possessive = []
                for te in text:
                    if te in self.personDict:
                        person = self.personDict[te]
                        if person == '1':
                            possessive = ['my']
                        elif person == '2':
                            possessive = ['your']
                        else:
                            possessive = ['their']
                        break
                    else:
                        possessive.append(te+"'s")
                self.parsed[i] = [possessive, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
            prevTags = []
            if not i == 0:
                prevTags = self.parsed[i-1][1]
            if '[NOUN]' in tags and '[POS]' not in prevTags:
                articled = []
                for te in text:
                    if te[0].islower():
                        articled.append("a "+te)
                    else:
                        articled.append(te)
                self.parsed[i] = [articled, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
            if '[OBJ]' in tags and '[NOUN]' not in prevTags and not len(prevTags) == 0:
                articled = []
                for te in text:
                    if te[0].islower() and not te[0:2] == "a ":
                        articled.append("a "+te)
                    else:
                        articled.append(te)
                self.parsed[i] = [articled, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
            if '[LOC]' in tags:
                articled = []
                for te in text:
                    articled.append("at "+te)
                self.parsed[i] = [articled, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
            if '[WANT]' in tags:
                articled = []
                for te in text:
                    articled.append("want to "+te)
                self.parsed[i] = [articled, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
            if '[NEG]' in tags:
                articled = []
                self.neg = True
                if '[PAST]' in tags:
                    for te in text:
                        articled.append("did not "+te)
                    self.parsed[i] = [articled, tags]
                else:
                    for te in text:
                        articled.append("do not "+te)
                    self.parsed[i] = [articled, tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
                
    
    def conjugateVerbs(self, verbs, tags):
        params = "3sg"
        person = "3"
        tense = "sg"
        conjugated = []
        past = False
        prog = False
        
        if '[PAST]' in tags:
            past = True
            
        if self.neg:
            past = False
            
        if '[PROG]' in tags:
            prog = True
        
        if self.subj in self.personDict:
            person = self.personDict[self.subj]
            
        if past:
            if prog:
                params = "ppart"
            else:
                if self.sing:
                    params = person+"sgp"
                else:
                    params = "ppl"
        else:
            if prog:
                params = "part"
            else:
                if self.sing:
                    params = person+"sg"
                else:
                    params = "pl"
            
        for word in verbs:
            if not prog:
                conjugated.append(str(pat.conjugate(word, params)))
            else:
                conjugated.append(str(self.conjugateBe(self.subj, not self.sing)+" "+pat.conjugate(word, params)))
            
        return conjugated
        
    def pluralize(self, words):
        plural = []
        for word in words:
            plural.append(pat.pluralize(word))
            
        return plural
        
    def interpretTags(self):
        for i in xrange(len(self.parsed)):
            word = self.parsed[i]
            text = word[0]
            tags = word[1]
            
            if text[0] == 'be':
                self.parsed[i] = [self.conjugateVerbs(text, tags), tags]
                word = self.parsed[i]
                text = word[0]
                tags = word[1]
            
            for tag in tags:
                if tag == '[PLR]':
                    self.sing = False
                    self.parsed[i] = [self.pluralize(text), tags]
                    
                if tag in self.verbMod:
                    self.parsed[i] = [self.conjugateVerbs(text, tags), tags]
    
    def parse(self):
        word = self.raw[0]
        tags = []
        for i in xrange(1, len(self.raw)):
            curr = self.raw[i]
            if curr[0][0] == '[':
                tags.append(curr[0])
            else:
                self.parsed.append([word, tags])
                tags = []
                word = curr
        
        self.parsed.append([word, tags])
    
    def __init__(self, obj=[]):
        self.parsed = []
        self.raw = obj
        self.sing = True
        self.que = False
        self.subj = ""
        self.neg = False
        
        self.parse()
        self.initialPass()
        self.interpretTags()
        
inputs = [[['I', 'me'], ['[WA]'], ['drink', 'gulp', 'swallow'], ['[WANT]'], ['milk'], ['[NOUN]'], ['[OBJ]']], [['Mr.', 'Ms.'], ['Robert'], [','], ['I', 'me'], ['[PLR]'], ['[WA]'], ['be', 'exist', 'live', 'have', 'be located', 'be equipped with', 'happen', 'come about'], ['test'], ['tomorrow'], ['[OBJ]']], [['I', 'me'], ['[WA]'], ['study'], ['[NEG]'], ['[PAST]'], ['Japanese'], ['[NOUN]'], ['yesterday'], ['[OBJ]']], [['this'], ['[WA]'], ['be'], ['I', 'me'], ['[POS]'], ['cute', 'adorable', 'charming', 'lovely', 'pretty', 'dear', 'precious', 'darling', 'pet', 'cute little', 'tiny'], ['pen']], [["Let's"], ['[WA]'], ['drink', 'gulp', 'swallow'], ['[VOL]'], ['[QUE]'], ['coffee'], ['[NOUN]'], ['coffee lounge', 'coffee shop', 'cafe'], ['[NOUN]'], ['[LOC]'], ['[OBJ]']], [["Let's"], ['[WA]'], ['study'], ['[VOL]'], ['together', 'at the same time', 'same', 'identical'], ['[DIR]'], ['library'], ['[NOUN]'], ['[LOC]']], [['such', 'like that', 'that sort of', 'very'], ['thing', 'matter', 'incident', 'occurrence', 'event', 'circumstances', 'situation', 'state of affairs', 'work', 'business', 'affair'], ['if', 'in case', 'if it is the case that', 'if it is true that', 'as for', 'on the topic of'], [','], ['cooperate'], ['happily'], ['[LOC]']], [['I', 'me'], ['[WA]'], ['help', 'assist', 'take part in'], ['he', 'him', 'his'], ['[OBJ]']], [['I'], ['[WA]'], ['teach', 'inform', 'instruct'], ['[PROG]'], ['university'], ['[NOUN]'], ['[LOC]']], [['Jason'], ['[NOUN]'], [','], ['hold', 'carry', 'possess'], ['[PROG]'], ['[QUE]'], ['family', 'members of a family'], ['[NOUN]'], ['[POS]'], ['photograph', 'photo', 'movie'], ['[NOUN]'], ['[OBJ]']]]

model = em.EnglishModel()
model.load_bigrams("./w2Caps")

for i in inputs:
    sen = Sentence(i)
    result =  model.rate_sentences(sen.noTags())[0][0]
    if result[-3:] == " ?.":
        result = result[:-3]+"?"
    print result
    print "_______________"