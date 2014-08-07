from __future__ import division
import nltk, re, pprint
from nltk.book import *
from urllib import urlopen
from nltk.corpus import PlaintextCorpusReader, stopwords
from HTMLParser import HTMLParser
from nltk.tokenize import *


#reads in all transcript files
corpus_root = 'C:\Users\Brent\Documents\The Test Vault\Spring Semester 2014\Big Data\stuff\RadioTranscripts'
wordlists = PlaintextCorpusReader(corpus_root, '.*')

class StaticVariables:
    #declares array for indices to be stored
    fileIDs = ""
    
    #goes through a specified number of 
    documentRangeBegin = 0
    documentRangeEnd = 0
    
    paragraphForm = False
    tokenizedForm = False

#sets to total number of transcript files
numberOfFiles = len(wordlists.fileids())
#Error-checking: print(numberOfFiles)

def readInFiles():
    #reads in indices for transcripts in order corresponding to president
    readInFileIDs = open("C:\Users\Brent\Documents\Big Data\stuff\AllRadiotxt.rtf", 'rU')
    readInFileIDs = readInFileIDs.read()
    #Error-checking: print(rea'C:\Users\Brent\Documents\My Research\Supreme Court Justices\Transcripts' + i, 'rU'dInFileIDs)
    
    #remove uneccessary strings
    editedFileIDs = readInFileIDs.split('\\par')
    
    
    #moves through all lines of the file
    for line in editedFileIDs:
        #strips file each iteration to only a single ID number
        currentFileID = line.strip()
        
        #this is then added to an array - fileIDs
        StaticVariables.fileIDs = StaticVariables.fileIDs + ' ' + currentFileID
        
    #removes more unecessary strings
    StaticVariables.fileIDs = StaticVariables.fileIDs.split('fs22', 1)[1]
    StaticVariables.fileIDs = StaticVariables.fileIDs.split('d\\', 1)[0]
    
    #tokenizes the file and sets each ID number in order according to an indice
    StaticVariables.fileIDs = nltk.word_tokenize(StaticVariables.fileIDs)
    #Error-checking: print(fileIDs[0:5])
    #Error-checking: print(len(fileIDs))

#possible erro checking to do later
#while True:
#    try:
#        numberOfFiles == len(fileIDs)
#        break
#    except FileError:
#            print "The Documents no longer in sync"


def Presidents(president): #sets appropriate range for chosen president
    if president == "Reagan":
        StaticVariables.documentRangeBegin = 0
        StaticVariables.documentRangeEnd = 333
    elif president == "Bush Sr":
        StaticVariables.documentRangeBegin= 334
        StaticVariables.documentRangeEnd = 351
    elif president == "Clinton":
        StaticVariables.documentRangeBegin= 352
        StaticVariables.documentRangeEnd = 760
    elif president == "Bush Jr":
        StaticVariables.documentRangeBegin= 761
        StaticVariables.documentRangeEnd = 1175
    elif president == "Obama":
        StaticVariables.documentRangeBegin= 1176
        StaticVariables.documentRangeEnd = 1439
    elif president == "All":
        StaticVariables.documentRangeBegin= 0
        StaticVariables.documentRangeEnd = 1439
    return

#to be done later for indicies
#def Presidents(firstIndex, secondIndex): #sets appropriate range for chosen president
#    StaticVariables.documentRangeBegin = firstIndex
#    StaticVariables.documentRangeEnd = secondIndex
#    return    


def displayType(formOfDisplay): #function for paragraph of tokenize
    if formOfDisplay == "paragraph":
        StaticVariables.paragraphForm = True
    elif formOfDisplay == "tokenize":
        StaticVariables.tokenizedForm = True 

def printTranscripts(convertLowerCase, printYES):
    global outputHTML
    global byTime

    byTime = []
    if (StaticVariables.paragraphForm == True):
        outputHTML = ''
    elif (StaticVariables.tokenizedForm ==True):
        outputHTML = []
    if (StaticVariables.paragraphForm or StaticVariables.tokenizedForm == True):
        for i in range(StaticVariables.documentRangeBegin, StaticVariables.documentRangeEnd):
            #temporary variable to store current ID at current indice
            currentFile = StaticVariables.fileIDs[i]
            #Error-checking: print(currentFile)
            
            #loads in and opens the appropriate url file
            url = "file:///C:/Users/Brent/Documents/Big%20Data/stuff/RadioTranscripts/RadioTranscript" + currentFile + ".html"
            html = '' + urlopen(url).read()

            #removes uneccessary strings
            html = html.split('<span class="displaytext">',1)[1]
            html = html.split('</span><hr noshade="noshade" size="1"><span class="displaynotes">',1)[0]
            html = nltk.clean_html(html)

            if (convertLowerCase == "Yes"):
                for word in html:
                    html = html.lower()
            
            html = ''.join(html)


            byTime.append(html)    
            #default paragraph form
            if StaticVariables.paragraphForm == True:
                outputHTML += html
            elif StaticVariables.tokenizedForm == True: 
                #prints transcirpt of presidents speech in tokenized form
                html = WhitespaceTokenizer().tokenize(html)
                outputHTML.extend(html)

    if (printYES == "Yes"):
        print(outputHTML)

def frequencyDistribution():
    global x 
    x = outputHTML
    #x = [w for w in outputHTML if not w in stopwords.words('english')]
    punctuation = re.compile(r'[-.?!,":;()|]')
    x = [punctuation.sub("", word) for word in outputHTML]   
    for word in x:
        wordReplacement = word
        
        #skipList = ['us', 'business', 'bless']
        #if word in skipList:
        #    continue
            
        index = x.index(word)

        for suffix in [',', '.']:
            if wordReplacement.endswith(suffix):
                wordReplacement = wordReplacement[:-len(suffix)]
                x.pop(index)
                x.insert(index, wordReplacement)        
            

    x = [w for w in outputHTML if not w in stopwords.words('english')]
    fhtml = FreqDist(x)
    fhtml.plot(50)
 
def conditionalFreqDist():
     cfd = nltk.ConditionalFreqDist((target, fileid) 
     for fileid in range(StaticVariables.documentRangeEnd - StaticVariables.documentRangeBegin)
     for word in WhitespaceTokenizer().tokenize(byTime[fileid])
     for target in ['russia', 'soviet']
     if word.lower().startswith(target))
     cumTest = raw_input("Cumulative? True or False: ")

     cfd.plot(cumulative = cumTest)
           
            
readInFiles()
print("Write Reagan, Bush Sr, Clinton, Bush Jr, Obama, or All")
Presidents(raw_input("Enter the president your interested in: "))
displayType(raw_input("Enter paragraph or tokenize: "))  
printTranscripts(raw_input("Would like to convert to all lower case words? "), 
                raw_input("Would you like to print this out? If so, type 'Yes': "))

if (raw_input("Would you like to analyze: ") == "Yes"):
    #this works best after tokenizing HTML
    frequencyDistribution()


