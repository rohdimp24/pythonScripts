
#now we need to find the bigrams
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.metrics import BigramAssocMeasures




def initialize():

    prefixpath="/Users/305015992/pythonProjects/wordcloud/"

    '''Read teh cases file. This is the raw cases containing the full data and not split at the sentence level'''
    fname=prefixpath+"all_jim_case_large.txt"
    with open(fname, 'r') as myfile:
        data=myfile.read()

    data=data.split('-------BREAK--------')
    cases=[case.strip() for case in data]
    print(cases[1:10])
    print(len(cases))
    lengthCases=len(cases)

    stopwordsFile = open(prefixpath+'stopwordsss.txt', 'r')
    stopwords=stopwordsFile.read()
    stopwordList=stopwords.split(",")

    domainFileName=prefixpath+'domainss.txt'
    # with open(domainFileName, 'r') as myDomainFile:
    #     domainFileData=myDomainFile.read()
    #
    # domainLines=domainFileData.split('\n')
    # print(domainLines[1])
    #
    # domainwordList=[domainLine.split(',') for domainLine in  domainLines]
    #
    # print(domainwordList[1:10])


    domainLines = [domainLine.rstrip('\n').split(',') for domainLine in open(domainFileName)]
    domainDict={}
    for dl in domainLines:
            key=dl[0].replace('"','')
            value=dl[1].replace('"','')
            domainDict[key]=value.strip()
            #unigramDict[str].replace('"','')
    #         ngramDict[str]=ll[2]

    return cases,stopwordList,domainDict

cases,stopwordList,domainDict=initialize()

import re
import numpy as np

lengthCases=len(cases)

cleanedUpCases=[]
for count in range(0,lengthCases):
    # print("before {}",case)
    case=cases[count]
    case=case.lower()
    case = case.strip();
    case = re.sub('/[^A-Za-z0-9 _\-\+\&\,\#]/', '', case)
    case = case.replace('"', ' ')
    case = case.replace('\"', ' ')
    case = case.replace('>', ' ')
    case = case.replace('@', ' ')
    case = case.replace('<', ' ')
    case = case.replace(':', ' ')
    case = case.replace('.', ' ')
    case = case.replace('(', ' ')
    case = case.replace(')', ' ')
    case = case.replace('[', ' ')
    case = case.replace(']', ' ')
    case = case.replace('_', ' ')
    case = case.replace(',', ' ')
    case = case.replace('#', ' ')
    case = case.replace('-', ' ')
    case = case.replace('/', ' ')
    case = case.replace('"', ' ')
    case = case.replace('\n', ' ')
    case = case.replace('~', ' ')
    case = re.sub(r'\d+', ' ', case)
    cleanedUpCases.append(case)

print(cleanedUpCases[1:20])
print(len(cleanedUpCases))

#now we want to create the dictionary based on the ngram analysis
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(min_df=0.001,stop_words=stopwordList,strip_accents='unicode',binary=False)
rawDtm = count_vect.fit_transform(cleanedUpCases)
#maximum is 4997
#rawDtm = vectorizer.fit_transform(cleanedUpCases[0:4900])
print("Data dimensions: {}".format(rawDtm.shape))

vocab=count_vect.get_feature_names()
print(len(vocab))

countDtm = rawDtm.toarray()
countDtm=np.array(countDtm)

freqsum=np.sum(countDtm,axis=0)

np.amax(freqsum)
np.amin(freqsum)


#TODO: convert this to a form dict[word]=value

freqDict={}
for idx,v in enumerate(vocab):
    #freqDict.append({'word':v,'count':freqsum[idx]})
    freqDict[v]=freqsum[idx]


print(freqDict)


'''creating the sorted list of the freqdict'''

# sorting the dictionary using the value ..http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
#there are multiple ways i am using the itemgetter way
sortedFreqDict=[]
for w in sorted(freqDict, key=freqDict.get, reverse=True):
    print(w, freqDict[w])
    #sortedFreqDict[]

sorted(freqDict.items(), key=lambda x: x[1])

from operator import itemgetter
sortedFreqDict=sorted(freqDict.items(), key=itemgetter(1),reverse=True)



def getFreqOfKeyword(freqDict,keyword):
    for key in freqDict:
        if(key==keyword):
            return(freqDict[key])

print(getFreqOfKeyword(freqDict,"disch"))


def getKeywordBasedOnFrequency(freqDict,freq):
    for key in freqDict:
        if (freqDict[key]==freq):
            return (key)

print(getKeywordBasedOnFrequency(freqDict,81))

#unigrams:
#list of unigrams
getKeywordBasedOnFrequency(np.amin(freqsum))
print(vocab)


#the list of unigrams
unigrams=vocab


#in addition to the unigrams found using the statistic count we need to add the POS variations as well



def get_bigrams(myString):
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(myString)
    cleanedTokens=[x for x in tokens if x.lower() not in stopwordList]
    # print(tokens)
    #stemmer = PorterStemmer()
    bigram_finder = BigramCollocationFinder.from_words(cleanedTokens)
    #bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5)
    #print(bigrams)

    # for bigram_tuple in bigrams:
    #     x = "%s %s" % bigram_tuple
    #     tokens.append(x)

    return bigram_finder.ngram_fd.items()
    # for k, v in bigram_finder.ngram_fd.items():
    #     key=(' '.join(k))
    #     if key not in bigramCounts.keys():
    #         bigramCounts[key]=v
    #     else:
    #         bigramCounts[key]+=v
    #
    # return bigramCounts



def get_trigrams(myString):
    #myString=cleanedUpCases[1]
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(myString)
    cleanedTokens=[x for x in tokens if x.lower() not in stopwordList]
    # print(tokens)
    #stemmer = PorterStemmer()
    trigram_finder = TrigramCollocationFinder.from_words(cleanedTokens)
    trigrams = trigram_finder.nbest(TrigramAssocMeasures.chi_sq, 5)
    #print(trigrams)

    return trigram_finder.ngram_fd.items()
    # for bigram_tuple in bigrams:
    #     x = "%s %s" % bigram_tuple
    #     tokens.append(x)

    # for k, v in trigram_finder.ngram_fd.items():
#         key=(' '.join(k))
#         #print(key)
# #        print(trigramCounts.keys())
#         if key not in trigramCounts.keys():
#             trigramCounts[key]=v
#
#         else:
#              trigramCounts[key]+=v
#
#     return trigramCounts


bigramFeatures=[]
for case in cleanedUpCases:
    #need to make sure that the case does not have stop words
    bigramFeatures.append(get_bigrams(case))

print(len(bigramFeatures))

bigramFeatures[1:10]
bigramCounts={}

for bigramFeature in bigramFeatures:
    for k, v in bigramFeature:
        key=(' '.join(k))
        if key not in bigramCounts.keys():
            bigramCounts[key]=v
        else:
            bigramCounts[key]+=v

len(bigramCounts)

finalBigramFeatures=[]
for key in bigramCounts:
    if(bigramCounts[key]>20):
        print(key)
        arrBigrams=key.split()
        if(arrBigrams[0]!=arrBigrams[1]):
            #iff the individual words are part of unigrams then only add it
            if((arrBigrams[0] in unigrams) and (arrBigrams[1] in unigrams)):
                finalBigramFeatures.append(key)

#finalBigramFeatures
len(finalBigramFeatures)



###same for the trigrams
trigramFeatures=[]
for case in cleanedUpCases:
    #need to make sure that the case does not have stop words
    trigramFeatures.append(get_trigrams(case))
print(len(trigramFeatures))

trigramCounts={}
for trigramFeature in trigramFeatures:
    for k, v in trigramFeature:
        key=(' '.join(k))
        if key not in trigramCounts.keys():
            trigramCounts[key]=v
        else:
            trigramCounts[key]+=v

len(trigramCounts)



finalTrigramFeatures=[]
for key in trigramCounts:
    if(trigramCounts[key]>20):
        print(key)
        arrTrigrams=key.split()
        if(arrTrigrams[0]!=arrTrigrams[1]!=arrTrigrams[2]):
            #iff the individual words are part of unigrams then only add it
            if((arrTrigrams[0] in unigrams) and (arrTrigrams[1] in unigrams) and (arrTrigrams[2] in unigrams)):
                finalTrigramFeatures.append(key)

#finalBigramFeatures
len(finalTrigramFeatures)


len(unigrams)
len(finalBigramFeatures)
len(finalTrigramFeatures)




###now we have to write the logic for the normaliza
#we will first find the stemming of the various unigrams and then create the dictionary that will map all of the unigrams to that

''''
The steps are as follows
1. First create a map of stem and all the words that match this stem e.g. 'increas': ('increase', 895, 'increasing', 676, 'increases', 313)
2. Create a word to stem mapping. e.g increase: increas
3. Create a map of final stem to word map that is all the words that match this stem should be replaced by this word e.g.
increas : increase
decreas: decreased

this will use the map that was created in step 1

4. now use the maps in step 2 and 3 to find the final dictionary
word1->stem
stem->normalizedword
will give
word1->nomralized word

increasing : increase
increases : increase


'''


from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
print(freqDict)
#stem->set of similar stemming words group
stemmingDictBasedOnFreq={}
for k,v in sortedFreqDict:
    print(k,v)
    # k=dict['word']
    # v=dict['count']
    stemKey=stemmer.stem(k)
    if (stemKey not in stemmingDictBasedOnFreq):
        stemmingDictBasedOnFreq[stemKey]=(k,v)
    else:
        stemmingDictBasedOnFreq[stemKey]+=(k,v)


print(stemmingDictBasedOnFreq)


#word->stem mapping
wordToStemMapping={}
for k,v in sortedFreqDict:
    print(k,v)
    # k=dict['word']
    # v=dict['count']
    stemKey=stemmer.stem(k)
    wordToStemMapping[k]=stemKey

print(len(wordToStemMapping))



#this is stem->finalword mapping
stemmingDictFinal={}
for k in stemmingDictBasedOnFreq:
    print(k)
    #take the fisrst entry from the list that is stored for each stem value
    stemmingDictFinal[k]=list(stemmingDictBasedOnFreq[k])[0]

stemmingDictFinal['rotor']

print(len(stemmingDictFinal))


# import pandas as pd
#
# pp = pd.DataFrame(list(zip(wordToStemMapping, stemmingDictFinal)), columns=['num of occurence', 'Number of such Keys'])

# print(pp)

'''This will perform the normalizations'''
#now we want to find the actual mapping for each unigram
normalizedUnigrams={}
for k in wordToStemMapping:
    stem=wordToStemMapping[k]
    print(k,stem,stemmingDictFinal[stem])
    normalizedUnigrams[k]=stemmingDictFinal[stem]

print(normalizedUnigrams)

#bring in the domain information as well
for k in normalizedUnigrams:
    for j in domainDict:
        if (k==j):
            print(k,j,domainDict[j])
            normalizedUnigrams[k]=domainDict[j]

print(normalizedUnigrams['pmp'])

def createNormalizedWordDict(DictTONormalize,normalizedUnigramDict,N):
    normalizedNgrams={}
    #perform it for the bigrams
    for k in DictTONormalize:
        arrgrams=k.split()
        str=''
        for i in range(N):
            str+=' '+normalizedUnigramDict[arrgrams[i]]
        normalizedNgrams[k]=str.strip()
    return normalizedNgrams

normalizedBigrams=createNormalizedWordDict(finalBigramFeatures,normalizedUnigrams,2)
normalizedTrigrams=createNormalizedWordDict(finalTrigramFeatures,normalizedUnigrams,3)

print(finalBigramFeatures)
print(len(finalBigramFeatures), len(normalizedBigrams))
print(normalizedBigrams)

print(len(finalTrigramFeatures), len(normalizedTrigrams))
print(normalizedTrigrams)

for k,v in normalizedTrigrams.items():
    print(k,v)


#combine the dictionaries as 1
finalNgram=normalizedUnigrams.copy()
finalNgram.update(normalizedBigrams)
finalNgram.update(normalizedTrigrams)

print(len(finalNgram))
print(finalNgram)

for k,v in finalNgram.items():
    if (k=="metal temp reading"):
        print(k,v)

#normalizedBigrams={}
# #perform it for the bigrams
# for k in finalBigramFeatures:
#     arrgrams=k.split()
#     normalizedBigrams[k]=normalizedUnigrams[arrgrams[0]]+' '+normalizedUnigrams[arrgrams[1]]
#
#
# print(len(finalBigramFeatures), len(normalizedBigrams))
# print(normalizedBigrams)


import pickle

output = open('outputDict.txt', 'ab+')
pickle.dump(finalNgram, output,protocol=0)
output.close()