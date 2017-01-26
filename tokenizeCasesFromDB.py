'''
This code will interface with the postgres database to read the raw cases and then write back the normalized cases to the db

the user need to specify which equipment typ cases are getting normalize.

'''

import psycopg2
#for some reason the user has to be postgres and not root
import csv


conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')


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

keywords=[]
keywordsRet=[]

def getCases(conn,equipmentType):
    #conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')
    cur = conn.cursor()
    #cur.mogrify("Select id,description from cases.smartsignal_jim_allfields where smartsignal_jim_allfields.equipmentType=%s",(equipmentType,))
    cur.execute("Select id,description from cases.smartsignal_jim_allfields where \"equipmentType\"=%s ",
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
    #equipmentType="FAN"
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
        #retWord=retWord+" "
    return (retWord)




import re
import json

def getNormalizedCases(conn,equipmentType):

    #equipmentType="FAN"
    cases,unigramDict,ngramDict=getIntiialize(conn,equipmentType)
    #print(cases)
    #print(ngramDict)
    # for key,value in cases.items():
    #     print(cases[key])
    arrUnigramFiltered = {}
    #startCaseNumber = 0
    #endCaseNumber = 100
    for key in cases:
        # print("before {}",case)
        #key=13157
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
        case = case.replace('\r', ' ')
        case = case.replace('%', ' ')
        case = case.replace('$', ' ')
        case = case.replace('!', ' ')
        case = case.replace('*', ' ')

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
                keywords.append(tempword)
                retWord = retWord.replace('"', '')
                keywordsRet.append(retWord)
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

            retWord = getNormalizedWord(tempword, ngramDict)
            if (retWord):
                #print("normalized",retWord)
                keywords.append(tempword)
                keywordsRet.append(retWord)
                str = str.replace(tempword, retWord)

        arrQuadgramFiltered[key]=str

    #print(arrQuadgramFiltered)
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

            retWord = getNormalizedWord(tempword, ngramDict)
            if (retWord):
                keywords.append(tempword)
                keywordsRet.append(retWord)
                #print("normalized tri",retWord)
                str = str.replace(tempword, retWord)

        arrTrigramFiltered[key]=str
    #print(arrTrigramFiltered)
    arrBigramFiltered = {}
    for key in arrTrigramFiltered:

        details = arrTrigramFiltered[key]
        arrTempTerms = details.split(" ")
        lenCase = len(arrTempTerms)
        str = ''
        #print(details);
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
            #print("tempword=>", tempword)
            retWord = getNormalizedWord(tempword, ngramDict)
            if (retWord):
                keywords.append(tempword)
                keywordsRet.append(retWord)
                #print("normalized", retWord)
                str = str.replace(tempword, retWord)
                #print("string:",str)

        arrBigramFiltered[key]=str
    #print(arrBigramFiltered)

    return (cases,arrUnigramFiltered,arrQuadgramFiltered,arrTrigramFiltered,arrBigramFiltered)

def printcases(cases,caseId,finalizedUnigrams,finalizedQuadgrams,finalizedTrigrams,finalizedBigrams):
    print(cases[caseId])
    print(finalizedUnigrams[caseId])
    print(finalizedQuadgrams[caseId])
    print(finalizedTrigrams[caseId])
    print(finalizedBigrams[caseId])





''''Main code that will insert the tokenized cases to db'''

'''


'''
'''
function to call the steps for each equipmenttype one by one
'''
equipmentType='FAN'
def test(equipmentType):
#equipmentType="FURNACE"


    print(equipmentType)
    cases,finalizedUnigrams,finalizedQuadgrams,finalizedTrigrams,finalizedBigrams=getNormalizedCases(conn,equipmentType)

    print(len(cases),len(finalizedUnigrams),len(finalizedQuadgrams),len(finalizedTrigrams),len(finalizedBigrams))

    # caseId=24
    #
    #printcases(caseId)
    #print(finalizedBigrams)
    #printcases(13157,cases,finalizedUnigrams,finalizedQuadgrams,finalizedTrigrams,finalizedBigrams)

    cur = conn.cursor()
    for key in cases:
        #print(cases[key])
        query = "INSERT INTO cases.smartsignal_normalized_case(id, \"originalCase\", \"normalizedCase\",\"equipmentType\") VALUES (%s, %s, %s,%s);"
        data = (key, cases[key], finalizedBigrams[key],equipmentType)
        cur.execute(query, data)

    conn.commit()


#test(equipmentType)
'''
the various equipment types are
1.FURNACE
2.HRSG
3.GEARBOX
4.CONDENSER
5.MILL
6.WIND_TURBINE
7.FEEDWATER_HEATER
8.SUBMERSIBLE_PUMP
9.RECIPROCATING_ENGINE
10.MOTOR
11.BOILER_FEED_PUMP
12.CHILLER
13.HOT_GAS_EXPANDER
14.GENERATOR
15.BLOWER
16.COMPRESSOR
17.LNG
18.HEAT_EXCHANGER
19.FAN
20.AIR_HEATER
21.NONE
'''


equips=[
  "GENERATOR",
  "LNG",
  "UNDEFINED",
  "HEAT_EXCHANGER",
  "PUMP",
  "STEAM_TURBINE",
  "FURNACE",
  "CONDENSER",
  "AIR_HEATER",
  "WIND_TURBINE",
  "COMBUSTION_TURBINE",
  "COOLING_TOWER",
  "NONE",
  "COMPRESSOR",
  "HOT_GAS_EXPANDER",
  "SUBMERSIBLE_PUMP",
  "BLOWER",
  "FEEDWATER_HEATER",
  "GEARBOX",
  "FAN",
  "MOTOR",
  "CHILLER",
  "RECIPROCATING_ENGINE",
  "MILL",
  "BOILER_FEED_PUMP",
  "HRSG"
]


for i in range(0,25):
    test(equips[i])



'''''
We are tryong to see if there are word that we are capturing as keword or the normalized word in the above step is actually from the
unigram and bigram dictioanry...can be ignored

'''


#print(keywords)
print(len(keywords))
myset = set(keywords)
print(len(myset))

mysetConverted=set(keywordsRet)
print(len(mysetConverted))

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

notFound=[]
for kk in mysetConverted:
    tt = my_in_array(kk, unigramDict, False)
    if (tt is None):
        print(kk)
        tt1 = getNormalizedWord(kk, ngramDict)
        if(tt1 is None):
            notFound.append(kk)


print(len(notFound))

convertedDict=[]
for key in ngramDict:
    convertedDict.append(ngramDict[key].replace(" ", "_", ))


equipmentType='FAN'
tokensToCheck=[]

cur = conn.cursor()
#cur.mogrify("Select id,description from cases.smartsignal_jim_allfields where smartsignal_jim_allfields.equipmentType=%s",(equipmentType,))
cur.execute("Select id,\"normalizedCase\" from cases.smartsignal_normalized_case where \"equipmentType\"=%s ",
            (equipmentType,))


rows = cur.fetchall()
for row in rows:
    print(row)
    arr=row[1].split()
    for rr in arr:
        if("_" in rr):
            print(rr)
            tokensToCheck.append(rr)



tokensToCheckSet=set(tokensToCheck)
#check for the values that are new
for key in tokensToCheckSet:
    if(key not in convertedDict):
        print(key)
