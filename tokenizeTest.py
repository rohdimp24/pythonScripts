import re
#read the entire file in a single shot.
#I have added the string ---break --- to demarcate the next case, since the newline is not working properly in php
prefixpath="/Users/305015992/pythonProjects/wordcloud/"

'''Read teh cases file. This is the raw cases containing the full data and not split at the sentence level'''
fname=prefixpath+"all_jim_case_large.txt"
with open(fname, 'r') as myfile:
    data=myfile.read()

data=data.split('-------BREAK--------')
cases=[case.strip() for case in data]
print(cases[1:10])

#print(data)

#cases = [line.replace('-------BREAK--------','') for line in open(fname) if(len(line)>5)]

print(len(cases))

#print(cases[1:10])

'''read the dictionary and split it on comma'''

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

#print(unigramDict)

'''Function to find if the word has a dictioary equivalent'''
def my_in_array(word,dictArr):
    # print(type(word))
    for idx,key in enumerate(dictArr):
        # print(key,word)
        if(key==word):
            # print(word)
            return(dictArr[key])
print(my_in_array("vlv",unigramDict))

def getNormalizedWord(word,ngramDict):
    retWord = my_in_array(word,ngramDict)
    if (retWord):
        retWord = retWord.replace(" ", "_", )
        retWord=retWord.replace('"','')
        retWord=retWord+" "
    return (retWord)

print(ngramDict)
print(getNormalizedWord("lube oil filter",ngramDict))

'''Replacing the unigrams with the dictionary '''
arrUnigramFiltered = []
startCaseNumber=0
endCaseNumber=500
for count in range(startCaseNumber,endCaseNumber):
    # print("before {}",case)
    case=cases[count]
    case = case.strip();
    case = re.sub('/[^A-Za-z0-9 _\-\+\&\,\#]/', '', case)
    case = case.replace('"', ' ')
    case = case.replace('\"', ' ')
    case = case.replace('>', ' ')
    case = case.replace('(', ' ')
    case = case.replace(')', ' ')
    case = case.replace('@', ' ')
    case = case.replace('<', ' ')
    case = case.replace(':', ' ')
    case = case.replace('.', ' ')
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

    print("after {}",case)

    # now once we have removed all the unwanted characters then we can start checking for the presence of teh unigrams

    arrTempTerms = case.split(" ")
    #print("the arrTempTerms is {}",arrTempTerms)
    #lenCase = len(arrTempTerms)
    #print(lenCase)
    # for term in arrTempTerms:
    #      print(term)

    str = ''
    for term in arrTempTerms:
        largestStringFound = ''
        firstword = term.lower()
        tempword = firstword
        # check if the word is present in Unigram dictionary
        print(firstword, tempword)
        retWord = my_in_array(tempword, unigramDict)

        print(retWord)
        if (retWord):
            retWord = retWord.replace('"', '')
            str += retWord+" "
            #print("skjhdksh");
            # echo "uni=>".$tempword."=>".$retWord."=>".$i."<br/>";
            #continue;
        else:
            if (len(tempword) >= 1):
                 str=str+tempword+" "
                #str = str.join(tempword)
    arrUnigramFiltered.append(str)


print(len(arrUnigramFiltered))
arrUnigramFiltered[3]

'''Functon to check on the trigrams..we will have to loop through the cases once again'''
# now the trigrams
arrTrigramFiltered=[]
#for case in cases[startCaseNumber:endCaseNumber]:
for count in range(startCaseNumber,endCaseNumber):
    print(count)
    details =arrUnigramFiltered[count]
    arrTempTerms = details.split(" ")
    lenCase = len(arrTempTerms)
    str=details;
    for i in range(lenCase):
        largestStringFound=''
        firstword=''
        secondword=''
        thirdword=''
        firstword=arrTempTerms[i].lower()
        if (i <= (lenCase-3)):
            secondword=arrTempTerms[i+1].lower()
            thirdword=arrTempTerms[i+2].lower()

        if (firstword == " " or secondword == " " or thirdword == " "):
            break;
        tempword = firstword+" "+secondword+" "+thirdword
        #tempword=tempword.strim()
        print("tempword=>",tempword)

        retword=getNormalizedWord(tempword,ngramDict)
        if (retword):
            print("normalized",retWord)
            str = str.replace(tempword, retword)

    arrTrigramFiltered.append(str)


print(arrTrigramFiltered[301])

'''now finally check for the bigrams'''
arrBigramFiltered=[]
for count in range(startCaseNumber,endCaseNumber):

    details =arrTrigramFiltered[count]
    arrTempTerms = details.split(" ")
    lenCase = len(arrTempTerms)
    str = ''
    # echo $details."<br/>";
    str=details;
    for i in range(lenCase):

        largestStringFound=''
        firstword=''
        secondword=''
        thirdword=''

        firstword=arrTempTerms[i].lower()
        if (i <= (lenCase-2)):
            secondword=arrTempTerms[i+1].lower()
        if (firstword == " " or secondword == " "):
            break
        tempword = firstword+" "+secondword
        print("tempword=>", tempword)
        retword = getNormalizedWord(tempword, ngramDict)
        if (retword):
            print("normalized", retWord)
            str = str.replace(tempword, retword)

    arrBigramFiltered.append(str)

print(arrBigramFiltered[301])

'''Finally print the original and the converted case'''

for i in range(startCaseNumber,endCaseNumber):
    print("original=>",cases[i])
    print("converted=>",arrBigramFiltered[i])

