'''
This code will interface with the postgres database to read the raw cases and then write back the normalized cases to the db

the user need to specify which equipment typ cases are getting normalize.

'''

import psycopg2
#for some reason the user has to be postgres and not root
import csv

conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')
equipmentType="WIND_TURBINE"


# cur = conn.cursor()
# cur.execute("Select id,description from cases.smartsignal_jim_allfields where \"equipmentType\"=%s",(equipmentType,))
# rows = cur.fetchall()
#
# cases={}
# #display the rows
# for row in rows:
#     print (row[0],row[1])
#     #cases[row[0]]={"original":row[1]}
#     cases[row[0]]=row[1]
#
# conn.commit()


def getCases(conn,equipmentType):
    #conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')
    cur = conn.cursor()
    #cur.mogrify("Select id,description from cases.smartsignal_jim_allfields where smartsignal_jim_allfields.equipmentType=%s",(equipmentType,))
    cur.execute("Select id,description from cases.smartsignal_jim_allfields where \"equipmentType\"=%s",
                (equipmentType,))

    rows = cur.fetchall()

    cases={}
    #display the rows
    for row in rows:
        #print (row[0],row[1])
        #cases[row[0]]={"original":row[1]}
        cases[row[0]]=row[1]

    return(cases)

def getIntiialize(conn,equipmentType):
	# fname = "all_jim_case_large.txt"
	# with open(fname, 'r') as myfile:
	# 	data = myfile.read()
    #
	# data = data.split('-------BREAK--------')
	# cases = [case.strip() for case in data]
	# #print(cases[1:10])
    cases=getCases(conn,equipmentType)
    dictFile = "/Users/305015992/pythonProjects/wordcloud/dict.csv"
    unigramDict = {}
    ngramDict = {}
    with open(dictFile, 'r') as csvfile:
        posReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in posReader:
            # print(row)
            # check for the presenc eof space
            if (len(row[0].split()) > 1):
                str = row[0]
                str = str.replace('"', '')
                ngramDict[str] = row[1].replace('"', '')
            else:
                str = row[0].replace('"', '')
                unigramDict[str] = row[1].replace('"', '')

    return (cases,unigramDict,ngramDict)



#getIntiialize()

def my_in_array(word,dictArr,isNgram):
    # print(type(word))
    for idx,key in enumerate(dictArr):
        # print(key,word)
        if(isNgram==True):
            if(dictArr[key]==word):
                return(dictArr[key])
        else:
            if(key==word):
                #print(word)
                return(dictArr[key])


def getNormalizedWord(word,ngramDict):
    retWord = my_in_array(word,ngramDict,True)
    if (retWord):
        retWord = retWord.replace(" ", "_", )
        retWord=retWord.replace('"','')
        retWord=retWord+" "
    return (retWord)




import re
import json

def getNormalizedCases(conn,equipmentType):

    cases,unigramDict,ngramDict=getIntiialize(conn,equipmentType)

    #print(unigramDict)
    # for key,value in cases.items():
    #     print(cases[key])
    arrUnigramFiltered = {}
    startCaseNumber = 0
    endCaseNumber = 100
    for key in cases:
        # print("before {}",case)
        case = cases[key]
        #print(case)
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

        # print("after {}",case)
        arrTempTerms = case.split(" ")
        #print(arrTempTerms)
        str = ''
        for term in arrTempTerms:
            largestStringFound = ''
            firstword = term.lower()
            tempword = firstword
            # check if the word is present in Unigram dictionary
            # print(firstword, tempword)
            retWord = my_in_array(tempword, unigramDict,False)

            #print(retWord)
            if (retWord):
                retWord = retWord.replace('"', '')
                str += retWord + " "
            else:
                if (len(tempword) >= 1):
                    str = str + tempword + " "
        arrUnigramFiltered[key]=str
    #print(arrUnigramFiltered)
    #print(cases[3073])

    arrQuadgramFiltered = {}
    # for case in cases[startCaseNumber:endCaseNumber]:
    for key in arrUnigramFiltered:
        # print(count)
        details = arrUnigramFiltered[key]
        arrTempTerms = details.split(" ")
        lenCase = len(arrTempTerms)
        str = details;
        for i in range(lenCase):
            largestStringFound = ''
            firstword = ''
            secondword = ''
            thirdword = ''
            fourthword = ''
            firstword = arrTempTerms[i].lower()
            if (i <= (lenCase - 4)):
                secondword = arrTempTerms[i + 1].lower()
                thirdword = arrTempTerms[i + 2].lower()
                fourthword = arrTempTerms[i + 3].lower()

            if (firstword == " " or secondword == " " or thirdword == " " or fourthword == " "):
                break;
            tempword = firstword + " " + secondword + " " + thirdword + " " + fourthword
            # tempword=tempword.strim()
            # print("tempword=>",tempword)

            retword = getNormalizedWord(tempword, ngramDict)
            if (retword):
                #print("normalized",retWord)
                str = str.replace(tempword, retword)

        arrQuadgramFiltered[key]=str

    arrTrigramFiltered = {}
    # for case in cases[startCaseNumber:endCaseNumber]:
    for key in arrQuadgramFiltered:
        # print(count)
        details = arrQuadgramFiltered[key]
        arrTempTerms = details.split(" ")
        lenCase = len(arrTempTerms)
        str = details;
        for i in range(lenCase):
            largestStringFound = ''
            firstword = ''
            secondword = ''
            thirdword = ''
            firstword = arrTempTerms[i].lower()
            if (i <= (lenCase - 3)):
                secondword = arrTempTerms[i + 1].lower()
                thirdword = arrTempTerms[i + 2].lower()

            if (firstword == " " or secondword == " " or thirdword == " "):
                break;
            tempword = firstword + " " + secondword + " " + thirdword
            # tempword=tempword.strim()
            # print("tempword=>",tempword)

            retword = getNormalizedWord(tempword, ngramDict)
            if (retword):
                #print("normalized tri",retWord)
                str = str.replace(tempword, retword)

        arrTrigramFiltered[key]=str

    arrBigramFiltered = {}
    for key in arrTrigramFiltered:

        details = arrTrigramFiltered[key]
        arrTempTerms = details.split(" ")
        lenCase = len(arrTempTerms)
        str = ''
        # echo $details."<br/>";
        str = details;
        for i in range(lenCase):

            largestStringFound = ''
            firstword = ''
            secondword = ''
            thirdword = ''

            firstword = arrTempTerms[i].lower()
            if (i <= (lenCase - 2)):
                secondword = arrTempTerms[i + 1].lower()
            if (firstword == " " or secondword == " "):
                break
            tempword = firstword + " " + secondword
            # print("tempword=>", tempword)
            retword = getNormalizedWord(tempword, ngramDict)
            if (retword):
                # print("normalized", retWord)
                str = str.replace(tempword, retword)

        arrBigramFiltered[key]=str

    return (cases,arrUnigramFiltered,arrQuadgramFiltered,arrTrigramFiltered,arrBigramFiltered)

print(equipmentType)
cases,finalizedUnigrams,finalizedQuadgrams,finalizedTrigrams,finalizedBigrams=getNormalizedCases(conn,equipmentType)

print(len(cases),len(finalizedUnigrams),len(finalizedQuadgrams),len(finalizedTrigrams),len(finalizedBigrams))

def printcases(caseId):
    print(cases[caseId])
    print(finalizedUnigrams[caseId])
    print(finalizedQuadgrams[caseId])
    print(finalizedTrigrams[caseId])
    print(finalizedBigrams[caseId])


caseId=24

printcases(caseId)


cur = conn.cursor()

for key in cases:
    #print(cases[key])
    query = "INSERT INTO cases.smartsignal_normalized_case(id, \"originalCase\", \"normalizedCase\",\"equipmentType\") VALUES (%s, %s, %s,%s);"
    data = (key, cases[key], finalizedBigrams[key],equipmentType)
    cur.execute(query, data)

conn.commit()





# cases,unigramDict,ngramDict=getIntiialize()
# arrTrigramFiltered = {}
# # for case in cases[startCaseNumber:endCaseNumber]:
# for key in finalizedQuadgrams:
#     # print(count)
#     details = finalizedQuadgrams[key]
#     arrTempTerms = details.split(" ")
#     lenCase = len(arrTempTerms)
#     str = details;
#     for i in range(lenCase):
#         largestStringFound = ''
#         firstword = ''
#         secondword = ''
#         thirdword = ''
#         firstword = arrTempTerms[i].lower()
#         if (i <= (lenCase - 3)):
#             secondword = arrTempTerms[i + 1].lower()
#             thirdword = arrTempTerms[i + 2].lower()
#
#         if (firstword == " " or secondword == " " or thirdword == " "):
#             break;
#         tempword = firstword + " " + secondword + " " + thirdword
#         # tempword=tempword.strim()
#         # print("tempword=>",tempword)
#
#         retword = getNormalizedWord(tempword, ngramDict)
#         if (retword):
#             # print("normalized tri",retWord)
#             str = str.replace(tempword, retword)
#
#     arrTrigramFiltered[key] = str
#
# print(len(arrTrigramFiltered))

#cases,unigramDict,ngramDict=getIntiialize()

#print(ngramDict)