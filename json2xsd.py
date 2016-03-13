# coding: utf-8
# Meant to be run with Python 3
import json
from collections import OrderedDict


INDENT = 2*' '

INDENTS = {'CLASS': 1*INDENT,
           'SEQUENCE': 2*INDENT,
           'ELEMENT': 3*INDENT,
           'SIMPLETYPE': 4*INDENT}



def getJson(filename):
    print('Reading JSON from file: %s' % filename)
    return json.load(open(filename), object_pairs_hook=OrderedDict)



def writeXSD(filename, jsonData):
    xsd = open(filename, 'w')
    
    writeHeader(xsd)
    writeClasses(xsd, jsonData)    
    writeFooter(xsd)
    
    xsd.close()



def writeClasses(outputFile, jsonData):
    print('Writing XSD classes')
    
    for className in jsonData.keys():
        writeClass(outputFile, className, jsonData[className])


        
def writeClass(outputFile, className, classDict):
    print('Writing class: %s' % className)
    
    outputFile.write('%s<xs:complexType name="%s">\n' % (INDENTS['CLASS'], className))
    outputFile.write('%s<xs:sequence>\n' % INDENTS['SEQUENCE'])
    
    # Write each element (class attribute)
    for element in classDict.keys():
        writeElement(outputFile, element, classDict[element])
    
    outputFile.write('%s</xs:sequence>\n' % INDENTS['SEQUENCE'])
    outputFile.write('%s</xs:complexType>\n' % INDENTS['CLASS'])
        
    
    
def writeElement(outputFile, elementName, elementDict):
    print('Writing element: %s' % elementName)
    
    occurs = elementDict['occurs'].split(',');
    
    try:
        minOccurs = occurs[0]
    except IndexError:
        minOccurs = 0
        
    try:
        maxOccurs = occurs[1]
    except IndexError:
        maxOccurs = 1

    print('occurs: %s' % occurs)
    print('min: %s; max: %s' % (minOccurs, maxOccurs))
    
    outputFile.write('%s<xs:element name="%s" minOccurs="%s" maxOccurs="%s">\n' % (INDENTS['ELEMENT'], elementName, minOccurs, maxOccurs))
    outputFile.write('%s<xs:simpleType>\n' % INDENTS['SIMPLETYPE'])
    outputFile.write('%s</xs:simpleType>\n' % INDENTS['SIMPLETYPE'])
    
    outputFile.write('%s</xs:element>\n' % INDENTS['ELEMENT'])
    
    #print(elementDict)
    
    
    
def writeHeader(outputFile):
    print('Writing XSD header')
    outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outputFile.write('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n')


    
def writeFooter(outputFile):
    print('Writing XSD footer') 
    outputFile.write('</xs:schema>\n')
    

    
if '__main__' == __name__:
    # Read JSON and write XSD
    writeXSD('newday.xsd', getJson('day.json'))

    # Run XJC tool to generate Java POJOs
