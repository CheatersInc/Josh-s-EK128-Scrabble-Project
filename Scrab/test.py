class ScrabbleHelper(self):
	def __init__(self):
		self.sfile=open('ospd.txt')
		self.lettersL=list(letters+wrapletter)
		self.scrabd={'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}
		self.hitlist={}
		self.wordlistd={}
	def test_words_in_textfile(self):
		for line in self.sfile:
			i=line.strip()
			if wrapletter in i and len(i)<=len(self.lettersL):
            	for char in i:
                	if char in lettersL and selflettersL.count(char)>=list(i).count(char):
                    	pass
                	else:
                    	basenum=0
                    	for let in i:
                        	basenum=basenum+scrabdict[let]
                    	hitlistd[i]=basenum
                    	break
                	basenum=0
                	for let in i:
                    	basenum=basenum+scrabdict[let]
                	wordlistd[i]=basenum
        	else:
            	pass
    def target_eliminate(self):
    	for word in self.hitlistd:
    		if word in self.wordlistd:
    			del wordlistd[word]
    def find_best_score(self):
    	bestplay=[]
    	bestscore=0
    	for word in wordlistd.keys():
        	if wordlistd[word]==bestscore:
            	bestplay.append(word)
        	elif wordlistd[word]<bestscore:
            	pass
        	else:
            	bestplay=[]
            	bestplay.append(word)
            	bestscore=wordlistd[word]			







