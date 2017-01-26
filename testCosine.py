
import numpy as np
import pandas as pd
import math


documents = (
"The sky is blue",
"The sun is bright",
"The sun in the sky is bright",
"We can see the shining sun, the bright sun"
)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

tfidf_matrix_dtm = tfidf_matrix.toarray()
tfidf_matrix_dtm=np.array(tfidf_matrix_dtm)
print(tfidf_matrix.shape)


from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
rawdtm = count_vect.fit_transform(documents)
vocab = count_vect.get_feature_names()
# convert the dtm to regular array
countDtm = rawdtm.toarray()
# convert the dtm to numpy array
countDtm = np.array(countDtm)
print(countDtm)
# need to convert it to numpy array so that we can easily perform the operations on it
vocab = np.array(vocab)

df=pd.DataFrame(tfidf_matrix_dtm,columns=vocab)
print(df)

print(tfidf_matrix[0:1])

def getAngleInRadian(cos_sim):
    # This was already calculated on the previous step, so we just use the value
    angle_in_radians = math.acos(float(cos_sim))
    return(math.degrees(angle_in_radians))

getAngleInRadian(0.54)
# import math
# # This was already calculated on the previous step, so we just use the value
# cos_sim = 0.52305744
# angle_in_radians = math.acos(cos_sim)
# print(math.degrees(angle_in_radians))
# 58.462437107432784

print(tfidf_matrix[0:3])


from sklearn.metrics.pairwise import cosine_similarity
sim_scores=cosine_similarity(tfidf_matrix[0:len(documents)], tfidf_matrix)
print(sim_scores)
print(sim_scores.tolist()[2])
results={}
for i in range(len(documents)):
    rr=[]
    for index,ss in enumerate(sim_scores.tolist()[i]):
        if(ss>1.0):
            ss=1.0
        if(ss<-1.0):
            ss=-1.0
        #print(index)
        #getAngleInRadian(ss)
        angle=getAngleInRadian(ss)
        print(ss,angle)
        rr.append({'caseId':index,'cosine':angle})
    results[i]=rr

import json
print(json.dumps(results))



