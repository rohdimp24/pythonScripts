import numpy as np

''' Reading the file to get teh cases'''
prefixpath="/Users/305015992/pythonProjects/wordcloud/"
fname=prefixpath+"output_autonormalizedjim_cases.txt"
lines = [line.rstrip('\\n') for line in open(fname)]
#print(lines[2:80])

#read the stop words
stopwordsFile = open(prefixpath+'stopwordsss.txt', 'r')
stopwords=stopwordsFile.read()
stopwordList=stopwords.split(",")


''' Performing the tfidf'''
from sklearn.feature_extraction.text import TfidfVectorizer
#we are taking normalization +
vectorizer = TfidfVectorizer(min_df=0.006,stop_words=stopwordList,strip_accents='unicode',norm='l2',sublinear_tf=True)
tfRawMatrix = vectorizer.fit_transform(lines[0:2000])
tfRawMatrix
print(tfRawMatrix)
print("Data dimensions: {}".format(tfRawMatrix.shape))
vectorizer.get_feature_names()
tfdtm = tfRawMatrix.toarray()
#convert the dtm to numpy array
tfdtm=np.array(tfdtm)
print(tfdtm)
tfVocab= np.array(vectorizer.get_feature_names())
print(tfVocab[79])

vectorizer._document_frequency()



tfdtm[1,204]


#?how come the tfIdf score for the idex 79 i.e. flatline =1

'''Performign the count vectorization which is same as finding the bag of words'''
from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer(min_df=0.006,stop_words=stopwordList,strip_accents='unicode',binary=False)
rawdtm = count_vect.fit_transform(lines[0:2000])
vocab=count_vect.get_feature_names()
#convert the dtm to regular array
dtm = rawdtm.toarray()
#convert the dtm to numpy array
dtm=np.array(dtm)

#need to convert it to numpy array so that we can easily perform the operations on it
vocab = np.array(vocab)


''' Testing the results of teh count vectorization '''

print("Data dimensions: {}".format(dtm.shape))
print("Data dimensions: {}".format(tfRawMatrix.shape))
print(rawdtm)
#print(vocab[1:20])
print(count_vect.vocabulary_.get("wind_speed"))
print(count_vect.vocabulary_.get("flatline"))
print(lines[0:10])
#dtm[:234]
print(vocab[67])

'''get the index of a particular word'''
turbine_idx = list(vocab).index('turbine')
print(turbine_idx)

tt=list(dtm[:,195]>0)
print(tt)
for idx,w in enumerate(tt):
    if(w==True):
        print(idx)



#get the indexes whose values are non zero in the dtm
def getkeywordsOfDocument(dtm,vocab,docNo):
    nn=np.flatnonzero(dtm[docNo,])
    print(nn)
    #print(nn[1])
    #get the corresponding word from the vocabulary list
    return(vocab[nn].tolist())

#lines[1]

#columm sum
freqsum=np.sum(dtm,axis=0)


'''to get the index for which the sum is maximum'''
'''cool way to get the index from the numpy array given the value list(freqsum).index(maxval)... this is equivalent to which'''
maxval=(freqsum[freqsum==max(freqsum)])[0]
print(maxval)
#myWhich(freqsum,max(freqsum))
max_idx=list(freqsum).index(maxval)
max_idx_word=vocab[max_idx]
print(max_idx_word)


# def myWhich(arr,val):
#     return (arr[arr == max(val)])


#myWhich(freqsum,max(freqsum))

def getFreqOfKeyword(freqDict,keyword):
    for key in freqDict:
        if(key['word']==keyword):
            return(key)




#for each of the vocabulary word create a dictionary containing the count
freqDict=[]
for idx,v in enumerate(vocab):
    freqDict.append({'word':v,'count':freqsum[idx]})

print(freqDict)

print(getFreqOfKeyword(freqDict,"flatline"))


#get the count of a particular word from the freqdict

# type(freqDict)
# freqDict.sort()


##I have the frequency count of the words. The DTM containes the document * terms matrix.
print(getkeywordsOfDocument(dtm,vocab,1))

import math

#the tf-idf by default is calcluated as tf : that is nuber of time the word has appeaered * (idf) which is
#idf = np.log(float(n_samples) / df) + 1.0
# in case of teh "flatline"
#tf=2
#the idf is 3.538 so the tfidf is 7.06

#if the nomrmalise is l2 then divide by the squraeroot . in case there is only one term then the output will be 1
#by default (norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)[source]

#if we use (norm=None, use_idf=True, smooth_idf=True, sublinear_tf=False)
#this is calculated as tf*(log(2000/158)+1)
#7.06

#if we use (norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
#in this cae the evry value is divided bby the length of the vector. SO if there is only one keyword then the tfidf weight will be 1

#if we use sublinear_tf=Ttue then tf will be calcualted as 1+log(tf) so
#(1+log(2))*(log(2000/158)+1)=5.98103925314


idf=np.log(float(2000) / 158) + 1.0
print(idf)
tf=1+np.log(2)
print(tf)
tf_idf=idf*tf
print(tf_idf)

np.flatnonzero(dtm[1,])


print(lines[0])

#print(tfdtm.cumsum())

type(tfdtm)
format(dtm.shape)
type(dtm)



####
#now kmeans
from sklearn.cluster import KMeans
km = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 1000, n_init = 20, verbose = True)
#you need to call the km.fit_predict so that the kmeans cane be run and then each of the points can be assigned a cluster index
km.fit_predict(tfRawMatrix)

#km.labels_ will contain the clusterid against wach case...bascially to see which label does a case id belong to


#code to draw the clusters for the documents...the important thing is to convert the sparse matrix to dense matrix
#http://stackoverflow.com/questions/28160335/plot-a-document-tfidf-2d-graph

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def plotCLusters(tfSparseMatrix,kmResults):
    X=tfSparseMatrix.todense()
    pca = PCA(n_components=2).fit(X)
    data2D = pca.transform(X)
    plt.scatter(data2D[:,0], data2D[:,1],c=kmResults.labels_)
    #plt.show()
    centers2D = pca.transform(kmResults.cluster_centers_)
    #plt.hold(True)
    plt.scatter(centers2D[:,0], centers2D[:,1],
                marker='x', s=200, linewidths=3, c='r')
    plt.show()



plotCLusters(tfRawMatrix,km)

##collect the lines of different clusters togetehr
#the text is a dictioanry that will collect the text from al the articles of the cluster
text={}
for i,cluster in enumerate(km.labels_):
    oneDocument = lines[i]
    if cluster not in text.keys():
        text[cluster] = oneDocument
    else:
        text[cluster] += oneDocument


cases={}
for i,cluster in enumerate(km.labels_):
    if cluster not in cases.keys():
        cases[cluster] = str(i)+","
    else:
        cases[cluster] += str(i)+","

print(cases)



print(text[2])

#distribution in the clusters
np.unique(km.labels_, return_counts=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk

keywords = {}
counts={}
#for cluster in range(3):
cluster=2
word_sent = word_tokenize(text[cluster].lower())
word_sent=[word for word in word_sent if word not in stopwordList]
freq = FreqDist(word_sent)
keywords[cluster] = nlargest(100, freq, key=freq.get)
counts[cluster]=freq

print(counts)
print(keywords.get(2))

set(keywords.get(0)).unique(set(keywords.get(1)))

len(set(keywords[0]).union(set(keywords[1])))

unique_keys={}
type(unique_keys)
#for cluster in range(3):
cluster=0
other_clusters=list(set(range(3))-set([cluster]))

keys_other_clusters=set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
unique=set(keywords[cluster])-keys_other_clusters
unique_keys[cluster]=nlargest(10, unique, key=counts[cluster].get)


print(unique_keys)





########testung..this is from https://github.com/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.11-K-Means.ipynb

from sklearn.datasets.samples_generator import make_blobs
X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=0)
plt.scatter(X[:, 0], X[:, 1], s=50);

print(X)

kmeans = KMeans(n_clusters=4)
kmResults=kmeans.fit(X)

#plotCLusters(X,kmeans.fit(X))
y_kmeans = kmeans.predict(X)

plt.scatter(X[:, 0], X[:, 1], c=kmResults.labels_, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);