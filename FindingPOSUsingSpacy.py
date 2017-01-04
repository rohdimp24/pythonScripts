from spacy.en import English

nlp = English()

prefixpath="/Users/305015992/pythonProjects/wordcloud/"

'''Read teh cases file. This is the raw cases containing the full data and not split at the sentence level'''
fname=prefixpath+"all_jim_case_large.txt"
with open(fname, 'r') as myfile:
    data=myfile.read()

data=data.split('-------BREAK--------')
cases=[case.strip() for case in data]
print(cases[1:10])


stopwordsFile = open(prefixpath+'stopwordsss.txt', 'r')
stopwords=stopwordsFile.read()
stopwordList=stopwords.split(",")


corpus = [
    u"I like green eggs and ham.",
    u"Gear bearing temperatures have increased to ~63C on tag IMS-GEN, ~58C on tag IMS-ROT, and ~76C on tag HS-ROT with the turbine running at full power from Aug. 19-22. Ambient was ~14-17C during this time",
    u"I ate his liver with some fava beans and a nice chianti.",
    u"Within the past 2 weeks, generator bearing temperature NDE has been exceeding the model estimate with a recent spike as high as ~78C with an estimate of ~56C",
    u"Gentlemen, you can't fight in here! This is the War Room!",
    u"displaCy uses CSS and JavaScript to show you how computers understand language",
    u"If you are looking for ransom, I can tell you I don't have money. But what I do have are a very particular set of skills, skills I have acquired over a very long career. Skills that make me a nightmare for people like you."
]


from nltk.tokenize import sent_tokenize, word_tokenize



docs = [nlp(d) for d in cases]

for idx, doc in enumerate(docs[1:10]):
    print(idx)
    print(doc)
    # print format(idx)

    for sent in doc.sents:
        # for each sentence, print the tokens and their original form,lemma, pos, penn pos tag, and constituent
        print(sent)
        for token in sent:
            print(token.orth_, token.lemma_, token.pos_, token.tag_, token.dep_)
    print("noun chunks")
    for np in doc.noun_chunks:
        print(np.text, "..", np.root.text)
# for vp in doc.verb_chunks:
#             print(vp.text,"..",vp.root.text)

def cleanupText(str):
    str = str.strip();
    str = re.sub('/[^A-Za-z0-9 _\-\+\&\,\#]/', '', str)
    str = str.replace('"', ' ')
    str = str.replace('\"', ' ')
    str = str.replace(')', ' ')
    str = str.replace('(', ' ')
    str = str.replace('>', ' ')
    str = str.replace('@', ' ')
    str = str.replace('<', ' ')
    str = str.replace(':', ' ')
    str = str.replace('.', ' ')
    str = str.replace('[', ' ')
    str = str.replace(']', ' ')
    str = str.replace('_', ' ')
    str = str.replace(',', ' ')
    str = str.replace('#', ' ')
    str = str.replace('-', ' ')
    str = str.replace('/', ' ')
    str = str.replace('"', ' ')
    str = str.replace('\n', ' ')
    str = str.replace('~', ' ')
    str = re.sub(r'\d+', ' ', str)
    word_sent = [word for word in str.lower().split(" ") if word not in stopwordList and len(word)>1]
    if (len(word_sent) > 2):
        finalSent = ' '.join(word_sent)
    else:
        finalSent=''

    return(finalSent.strip())


'''This is the main function that is finding the noun phrases and creating a list of list'''
arrNounPhrase=[]
for idx, doc in enumerate(docs):
    testDoc=doc
    token_nounPhrases = [np.text for np in testDoc.noun_chunks]

    updatedNounPhrases=[]
    for tt in token_nounPhrases:
        # word_sent = [word for word in tt.lower().split(" ") if word not in stopwordList]
        # if(len(word_sent)>2):
        #     finalSent=' '.join(word_sent)
        #     updatedNounPhrases.append(finalSent)
        finalSent=cleanupText(tt)
        if(len(finalSent)>0):
            updatedNounPhrases.append(finalSent)
    arrNounPhrase.append(updatedNounPhrases)

print(arrNounPhrase)
# gg="o cooler outlet temperature"
# gg='1'
# print(len(gg))
# word_sent = [word for word in gg.lower().split(" ") if word not in stopwordList]
# print(word_sent)
'''function to flatten a list of list'''
''' this has been taken from http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python'''

flatten = lambda l: [item for sublist in l for item in sublist]
flatNounPhraseList=flatten(arrNounPhrase)
len(flatNounPhraseList)


'''Now we need to tabulate the results'''
nounPhraseDictCount={}
import re
#now we can apply the cleanup
for tt in flatNounPhraseList:
    finalSent=tt
    if (nounPhraseDictCount.get(finalSent)):
        nounPhraseDictCount[finalSent] += 1
    else:
        nounPhraseDictCount[finalSent] = 1

print(len(nounPhraseDictCount))

'''out of all the nounphrases pick up the once which are more frequncet'''
finalPOSList={}
for dd in nounPhraseDictCount:
    ddArr=dd.split(" ")
    if(len(ddArr)>1):
        #atelaset 10 occurence of the phrase
        if(nounPhraseDictCount[dd]>9):
            print(dd,nounPhraseDictCount[dd])
            finalPOSList[dd]=nounPhraseDictCount[dd]
            #finalPOSList.append()

print(len(finalPOSList))

print(finalPOSList)
ngramList=[]
#print only the keys i.e. the name of the ngram
for key,value in finalPOSList.items():
    print(key)
    ngramList.append(key)

#i guess we need to apply the domain knowldege and also see how we will map to the correct version
'''If we use the noun phrase to collect all the nouns ..remove the ones which have digits in them or special characters'''
##TODO::need to tabulate the dictionary to see what is the range of the count. I have put 3 as the min count but it might be not sufficent
# basically it should come some percentage times of the entire corpus

import numpy as np

#print(np.amax(np.asarray(finalPOSList)))
#this is the way to find the max, min and basically the range of the values
statArr=[]
for key,value in finalPOSList.items():
    statArr.append(value)

#get the range of the values
nparray=np.asarray(statArr)
maxVal=np.amax(nparray)
minVal=np.amin(nparray)
print(maxVal,"....",minVal)

#This is to tabulate
def getFreqDistribution():
    unique, counts = np.unique(nparray, return_counts=True)
    #print(np.asarray(unique,counts).T)
    return(unique,counts)


unique,counts=getFreqDistribution()
import pandas as pd
pp=pd.DataFrame(list(zip(unique,counts)),columns=['num of occurence','freq'])
print(pp.sort())



def getKeysBasedOnValue(val):
    indexes=[]

    for i in range(len(nparray)):
        if (nparray[i]==val):
            print(list(finalPOSList.keys())[i])
            #indexes.append(i)
    #return (indexes)



indexes=getKeysBasedOnValue(10)
# for i in indexes:
#     print(list(finalPOSList.keys())[i])
#
# maxIndex=list(nparray).index(4)
#
#
# list(finalPOSList.keys())[maxIndex]



##################EXTRA#########
'''want to check if there are words that are not present in the unigrams.If that is the case then we need to add those words in the unigrams'''
dictFile=prefixpath+"keywordMapping_jim.csv"
dictLines = [dictLine.rstrip('\n').split(',') for dictLine in open(dictFile)]
unigramDict={}
ngramDict={}
for ll in dictLines:
    #check for the presenc eof space
    if(len(ll[2].split())>1):
        str=ll[1]
        str=str.replace('"','')
        ngramDict[str]=ll[2]
        #ngramDict[ll[1]]=ll[2].replace(" ","_")
        #ngramDict[ll[1]].replace('"','')
    else:
        str=ll[1]
        str=str[1:-1]
        unigramDict[str]=ll[2]
        unigramDict[str].replace('"','')





def my_in_array(word,dictArr):
    # print(type(word))
    for idx,key in enumerate(dictArr):
        # print(key,word)
        if(key==word):
            # print(word)
            return(dictArr[key])



#check which of the ngramList is already present in the ngramDict
notinPrevDict=[]
for nn in ngramList:
    nn=nn.replace('  ',' ')
    retword=my_in_array(nn,ngramDict)
    if(retword==None):
        notinPrevDict.append(nn)





#check which all unigrams are not in the dictionary. Add those unigrams in the dictionary
for uu in ngramList:
    #uu=ngramList[1]
    words=uu.split(" ")
    if(len(words)>3):
        print(uu)
    #print(words)
    for word in words:
        if(len(word)>1):
            retword=my_in_array(word,unigramDict)
            if(retword==None):
                #print(word)
                #add to the unigram dictionary
                notinPrevDict.append(word)
                unigramDict[word]=word




len(notinPrevDict)
print(notinPrevDict)


print(unigramDict)

finalAdditionToDict=[]
## we need to add them to the dictionary.. so we need the canonical form
for nn in notinPrevDict:
    words = nn.split(" ")
    print(words)
    str=''
    for word in words:
        retword=my_in_array(word,unigramDict)
        if(retword):
            retword = retword.replace('"', '')
            str += retword + " "
    print(nn,"...",str)
    finalAdditionToDict.append(str)


#this is the list of the new dictioanry words that need to be added to the existing dictionary
for nn in finalAdditionToDict:
    print(nn)

