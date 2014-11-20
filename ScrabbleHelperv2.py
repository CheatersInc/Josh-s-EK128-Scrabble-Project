
# coding: utf-8

# In[193]:

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
    L=list(word)
    L.reverse()
    basestr=''
    for i in L:
        basestr=basestr+i
    d={}
    basenum=0    
    for i in basestr:
        if i in d:
            pass
        else:
            d[i]=basenum
        basenum=basenum+1
    return(d[wrapletter])

def letter_placement(letterscoreplacement,wrapletter,word):
    #determines what letter is in letterscoreplacement#
    L=list(word)
    afl=test_afl(wrapletter,word)
    bfl=test_bfl(wrapletter,word)
    if letterscoreplacement>0:
        return(L[len(word)-afl-1-letterscoreplacement])
    else: #letterscoreplacement<0
        return(L[len(word)-afl-1-letterscoreplacement])

def ScrabbleHelperBaseF(wrapletter,letters,beforewrapletter=10,afterwrapletter=10,wordscoremod=1,wordscoreplacement=100,letterscoremod=[],letterscoreplacement=[]):
    #Is base function for ScrabbleHelper
    #OSPD is the official scrabble word list#
    #afterletter and beforeletter are int referencing spaces available
    #on board relative to wrapletter (up/left for before, down/right for after)#
    #wordscoremod is the Word Score Modifier (Triple or Double), if it exists#
    #wordscoreplacement is placement of mod tile relative to wrapletter (positive is up/left;
    #negative is down/right) expressed as int number of spaces#
    #letterscoremod/placement works same as with word, but only for a particular letter,
    #and LSP/LSM is a list, in case of multiple LSM spaces#
    sfile=open('ospd.txt')
    #wrapletter=wr
    #wrapletter=wrapletter.upper()
    lettersL=list(letters+wrapletter)
    scrabdict={'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,
               'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10,'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,
               'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,
               'V':4,'W':4,'X':8,'Y':4,'Z':10}
    hitlistd={}
    wordlistd={}
    #analyzes each word in OSPD#
    for line in sfile:
        i=line.strip()
        #for word in all_variants(wrapletter,i):
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
                    basenum=basenum+scrabdict[let]
            #Double/Triple Letter Modifier#
            if len(letterscoreplacement)>1:
                for num in range(len(letterscoreplacement)):
                    if letterscoreplacement[num]==0:
                        basenum=basenum+scrabdict[wrapletter]*(letterscoremod[num]-1)
                    #test that word lands on letter modifier
                    elif letterscoreplacement[num]>0 and letterscoreplacement[num]>test_bfl(wrapletter,i):
                        pass
                    elif letterscoreplacement[num]<0 and letterscoreplacement[num]*-1>test_afl(wrapletter,i):
                        pass
                    else:
                        basenum=basenum+scrabdict[letter_placement(letterscoreplacement[num],wrapletter,i)]*(letterscoremod[num]-1)
            elif len(letterscoreplacement)==1:
                if letterscoreplacement[0]==0:
                    basenum=basenum+scrabdict[wrapletter]*(letterscoremod[0]-1)
                #test that word lands on letter modifier
                elif letterscoreplacement[0]>0 and letterscoreplacement[0]>test_bfl(wrapletter,i):
                    pass
                elif letterscoreplacement[0]<0 and letterscoreplacement[0]*-1>test_afl(wrapletter,i):
                    pass
                else:
                    basenum=basenum+scrabdict[letter_placement(letterscoreplacement[0],wrapletter,i)]*(letterscoremod[0]-1)
            else:
                pass
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


def ScrabbleHelperV2(wrapletters,letters,BWL=10,AWL=10,WSM=1,WSP=100,LSM=[],LSP=[]):
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


# In[194]:

import time
x=time.time()
print(ScrabbleHelperV2('a','abalone'))
y=time.time()
print(y-x)


# In[198]:

def all_variants(wrapletter,word):
    R=[]
    R.append(word.upper(wrapletter))
    return(R)
    
    #creates all variants indicating wrap letter, i.e.; t, tattle -> [Tattle, taTtle, tatTle]
    '''L,R,base=list(word),[],{}
    for i in range(len(word)):
        if L[i] in base:
            base[L[i]].append(i)
        else:
            base[L[i]]=[i]
    print(base)
    for let in base.keys():
        if let==wrapletter:'''
            
    
all_variants('r','arrow')


# In[178]:

the_list = ['albert', 'angela', 'leo', 'bridget']
[ word.upper().replace('A', 'a') for word in the_list]


# In[ ]:



