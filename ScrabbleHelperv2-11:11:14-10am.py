
# coding: utf-8

# In[10]:

def test_bfl(wrapletter,word):
    #determines number of characters left/up relative to wrapletter
    d={}
    basenum=0    
    for i in word:
        d[i]=basenum
        basenum=basenum+1
    return(d[wrapletter])

def test_afl(wrapletter,word):
    #determines number of characters right/down relative to wrapletter
    d={}
    basenum=0
    for i in word:
        d[i]=basenum
        basenum=basenum+1
    return(basenum-d[wrapletter]-1)

def place_in_word(letter,word):
    #determines place, as integer, of a letter in a word; i.e., in 'word', r is 3#
    resultL=[]
    basenum=0
    for char in word:
        if char==letter:
            basenum=basenum+1
            resultL.append(basenum)
        else:
            basenum=basenum+1
    return(resultL)

def ScrabbleHelperBaseF(wrapletter,letters,beforewrapletter=10,afterwrapletter=10,wordscoremod=1,wordscoreplacement=100,letterscoremod=1,letterscoreplacement=100):
    #Is base function for ScrabbleHelper
    #OSPD is the official scrabble word list#
    #afterletter and beforeletter are int referencing spaces available
    #on board relative to wrapletter (up/left for before, down/right for after)#
    #wordscoremod is the Word Score Modifier (Triple or Double), if it exists#
    #wordscoreplacement is placement of mod tile relative to wrapletter (positive is up/left;
    #negative is down/right) expressed as int number of spaces#
    #letterscoremod/placement works same as with word, but only for a particular letter#
    sfile=open('ospd.txt')
    lettersL=list(letters+wrapletter)
    scrabdict={'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}
    hitlistd={}
    wordlistd={}
    #analyzes each word in OSPD#
    for line in sfile:
        i=line.strip()
        #checks word length, AFL/BFL, and presense of wrapletter#
        if wrapletter in i and len(i)<=len(lettersL)  and test_bfl(wrapletter,i)<=beforewrapletter and test_afl(wrapletter,i)<=afterwrapletter:
            for char in i:
                #checks all char in word are also in lettersL + number of chars <= number of chars 
                #in lettersL; if not, adds to hitlist for later termination#
                if char in lettersL and lettersL.count(char)>=list(i).count(char):
                    pass
                else:
                    basenum=0
                    for let in i:
                        basenum=basenum+scrabdict[let]
                    hitlistd[i]=basenum
                    break
                #creates score associated with word in dictionary#
                basenum=0
                for let in i:
                    #test for letter score modifer#
                    if letterscoreplacement>0 and place_in_word(let,i)[0]==10000:
                        basenum=basenum+(scrabdict[let]*letterscoremod)
                    elif letterscoreplacement<0 and place_in_word(let,i)[0]==10000:
                        basenum=basenum+(scrabdict[let]*letterscoremod)
                    else:
                        basenum=basenum+scrabdict[let]
            #Double/Triple/Quadruple/6tuple/9tuple word modifier#
            if wordscoreplacement>=0 and test_bfl(wrapletter,i)>=wordscoreplacement:
                basenum=basenum*wordscoremod
            elif wordscoreplacement<=0 and test_afl(wrapletter,i)<=(wordscoreplacement*-1):
                basenum=basenum*wordscoremod
            else:
                pass
            #50 point bonus if all letters used#
            if len(i)==len(lettersL) and list(sorted(i))==sorted(lettersL):
                basenum=basenum+50
            #word:score#
            wordlistd[i]=basenum
        else:
            pass
    #termination script#
    for word in hitlistd:
        if word in wordlistd:
            del wordlistd[word]
    #determining best word; returns result in dictionary with key=int score#
    topplay=[]
    topscore=0
    for word in wordlistd.keys():
        if wordlistd[word]==topscore:
            topplay.append(word)
        elif wordlistd[word]<topscore:
            pass
        else:
            topplay=[]
            topscore=wordlistd[word]
            topplay.append(word)
    return([topplay,topscore])


def ScrabbleHelperV2(wrapletters,letters,BWL=10,AWL=10,WSM=1,WSP=100,LSM=1,LSP=100):
    #creates for loop to run SHBF with multiple wrapletters
    #and picks out best word given wrapletters#
    #arconyms refer to inputs of SHBF#
    topwordsd={}
    #creates dictionary containing words and their associated scores#
    for wrapchar in wrapletters:
        topwordsd[tuple(ScrabbleHelperBaseF(wrapchar,letters,BWL,AWL,WSM,WSP,LSM,LSP)[0])]=ScrabbleHelperBaseF(wrapchar,letters,BWL,AWL,WSM,WSP,LSM,LSP)[1]
    bestplay=[]
    bestscore=0
    #looks through aforementioned dictionary for best word based on score#
    for word in topwordsd.keys():
        if topwordsd[word]==bestscore:
            bestplay.append(word)
        elif topwordsd[word]<bestscore:
            pass
        else:
            bestplay=[]
            bestscore=topwordsd[word]
            bestplay.append(word)
    return([bestplay,bestscore])
    


# In[11]:

import time
x=time.time()
print(ScrabbleHelperV2('a','abalone',4,3,3,2))
y=time.time()
print(y-x)


# In[12]:

place_in_word('a','abalone')


# In[ ]:



