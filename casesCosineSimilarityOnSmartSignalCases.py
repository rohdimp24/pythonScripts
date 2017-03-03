'''
The script will find the cosine similarity between the cases. The user needs to provide the normalized cases per equipment type
I guess this is duplicate with the casesCosineSimilarity.py
'''

import numpy as np
from sklearn.cluster import KMeans
import psycopg2
import json
import pickle
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import json
import math

#for some reason the user has to be postgres and not root
'''Db connection'''
conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')


'''
Function Name:getIntiialize
Purpose: Reading teh normalized cases based on teh equipment type
Variables:
    -conn: the connection object
    -equipmentType: The category of cases

'''

def getIntiialize(conn,equipmentType):
    cur = conn.cursor()
    # cur.mogrify("Select id,description from cases.smartsignal_jim_allfields where smartsignal_jim_allfields.equipmentType=%s",(equipmentType,))
    cur.execute("SELECT id, \"originalCase\", \"normalizedCase\", "
                "\"possibleCause\",  \"equipmentType\" FROM cases.smartsignal_normalized_case where \"equipmentType\"=%s",(equipmentType,))

    rows = cur.fetchall()

    cases = {}
    causes={}
    # display the rows
    for row in rows:
        # print (row[0],row[1])
        # cases[row[0]]={"original":row[1]}
        cases[row[0]] = {"original":row[1],"normalized":row[2],"solution":row[3]}
        #causes[row[0]] = {"original":row[3],"normalized":row[4]}

    stopwordsFile = open('/Users/305015992/pythonProjects/wordcloud/stopwordsss.txt', 'r')
    stopwords = stopwordsFile.read()
    stopwordList = stopwords.split(",")

    return (cases,stopwordList)


'''
Convert from the cosine score to degree radians
'''
def getAngleInRadian(cos_sim):
    # This was already calculated on the previous step, so we just use the value
    angle_in_radians = math.acos(float(cos_sim))
    return (math.degrees(angle_in_radians))


'''
Function Name: findCosineSimilarity
Purpose: This is the main workhorse fucntion
does the following:
1. creates a tfidf matrix on the baseis of the various normalized cases
2. Currently it is not removing any word .(the df is not defined)
3. calculates the cosine score between all the documents. We are considering only those combinations where the score <75 degree
4. return the results

'''
def findCosineSimilarity(equipmentType):

    casesDict,stopwordList=getIntiialize(conn,equipmentType)
    print(len(casesDict))


    lines = []
    countToCaseIdMap={}
    # # maximum is 4997
    count=0
    for key in casesDict:
        lines.append(casesDict[key]['normalized'])  # now we need to vectorize the corpus
        countToCaseIdMap[count] = key
        count=count+1

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwordList, strip_accents='unicode')
    tfidf_matrix = tfidf_vectorizer.fit_transform(lines)

    tfidf_matrix_dtm = tfidf_matrix.toarray()
    tfidf_matrix_dtm=np.array(tfidf_matrix_dtm)
    print(tfidf_matrix.shape)


    '''unconmmen the following to see the distribution in the tfidf matrix using the pandas'''
    # from sklearn.feature_extraction.text import CountVectorizer
    # count_vect = CountVectorizer(stop_words=stopwordList, strip_accents='unicode')
    # rawdtm = count_vect.fit_transform(lines)
    # vocab = count_vect.get_feature_names()
    # # convert the dtm to regular array
    # countDtm = rawdtm.toarray()
    # # convert the dtm to numpy array
    # countDtm = np.array(countDtm)
    # #print(countDtm)
    # # need to convert it to numpy array so that we can easily perform the operations on it
    # vocab = np.array(vocab)
    # df = pd.DataFrame(tfidf_matrix_dtm, columns=vocab)
    # print(df)




    from sklearn.metrics.pairwise import cosine_similarity


    sim_scores=cosine_similarity(tfidf_matrix[0:len(lines)], tfidf_matrix)
    print(sim_scores)
    #ll=sim_scores.tolist()[0]
    #[i for i, e in sim_scores.tolist()[0] if e != 0.0]


    results = {}
    for i in range(len(lines)):
        rr = []
        print("check for ",i)
        for index, ss in enumerate(sim_scores.tolist()[i]):
            if (ss > 1.0):
                ss = 1.0
            if (ss < -1.0):
                ss = -1.0
            # print(index)
            # getAngleInRadian(ss)
            angle = getAngleInRadian(ss)
            if(angle<75.0):
                # print(ss, angle)
                caseId=countToCaseIdMap[index]
                rr.append({'caseId': caseId, 'cosine': angle,'description':casesDict[caseId]['original'],
                           'solution':casesDict[caseId]['solution']})
        results[countToCaseIdMap[i]] = rr

    return(results)


# print(json.dumps(results))

equipments=['CONDENSER','PUMP','COMPRESSOR','UNDEFINED','MOTOR','RECIPROCATING_ENGINE']

for i in range(len(equipments)):
    equipmentType=equipments[i]
    results=findCosineSimilarity(equipmentType)

    # dump the json to a file
    prefix="/Users/305015992/pythonProjects/wordcloud/"
    fname=prefix+"cosineScores_"+equipmentType+".json"
    #outF = open("/Users/305015992/pythonProjects/wordcloud/cosineScores_CT.json", "w")
    outF = open(fname, "w")
    outF.write(json.dumps(results))
    outF.close()



#enter into db


