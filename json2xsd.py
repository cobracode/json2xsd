# coding: utf-8
# Meant to be run with Python 3
import json
from collections import OrderedDict


INDENT = 2*' '

INDENTS = {'CLASS': 1*INDENT,
           'SEQUENCE': 2*INDENT,
           'ELEMENT': 3*INDENT,
           'SIMPLETYPE': 4*INDENT,
           'RESTRICTION': 5*INDENT,
           'RESTRICTIONS': 6*INDENT}



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

    defaultMin = 0
    defaultMax = 1

    try:
        occurs = elementDict['occurs'].split(',');

        try:
            minOccurs = occurs[0]
        except IndexError:
            minOccurs = defaultMin

        try:
            maxOccurs = occurs[1]
        except IndexError:
            maxOccurs = defaultMax

    except KeyError as e:
        minOccurs = defaultMin
        maxOccurs = defaultMax

    outputFile.write('%s<xs:element name="%s" minOccurs="%s" maxOccurs="%s">\n' % (INDENTS['ELEMENT'], elementName, minOccurs, maxOccurs))
    outputFile.write('%s<xs:simpleType>\n' % INDENTS['SIMPLETYPE'])

    writeRestrictions(outputFile, elementDict['type'], getRestrictions(elementDict))

    outputFile.write('%s</xs:simpleType>\n' % INDENTS['SIMPLETYPE'])
    outputFile.write('%s</xs:element>\n' % INDENTS['ELEMENT'])


def writeRestrictions(outputFile, type, restrictions):
    outputFile.write('%s<xs:restriction base="xs:%s">\n' % (INDENTS['RESTRICTION'], type))

    for restriction in restrictions:
        outputFile.write('%s<xs:%s value="%s" />\n' % (INDENTS['RESTRICTIONS'], restriction[0], restriction[1]))

    outputFile.write('%s</xs:restriction>\n' % INDENTS['RESTRICTION'])


def getRestrictions(elementDict):
    print('Checking element restrictions')

    restrictions = []
    restrictionTypes = ['length',
                        'minInclusive',
                        'maxInclusive',
                        'minExclusive'
                        'maxExclusive',
                        'maxLength',
                        'minLength',
                        'pattern',
                        'totalDigits',
                        'whitespace']

    for type in restrictionTypes:
        if type in elementDict:
            if type == 'whitespace':
                xsdType = 'whiteSpace'

            restrictions.append((xsdType, elementDict[type]))

    # Check for custom 'range' restriction
    if 'range' in elementDict:
        rangeList = elementDict['range'].split(',')
        restrictions.append(('minInclusive', rangeList[0]))
        restrictions.append(('maxInclusive', rangeList[1]))

    return restrictions


def writeHeader(outputFile):
    print('Writing XSD header')
    outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outputFile.write('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n')



def writeFooter(outputFile):
    print('Writing XSD footer')
    outputFile.write('</xs:schema>\n')




if '__main__' == __name__:
    try:
        # Read JSON and write XSD
        writeXSD('schema.xsd', getJson('schema.json'))
    except BaseException as e:
        # Handle uncaught exceptions
        print('Error: %s' % e)

    # Run XJC tool to generate Java POJOs
