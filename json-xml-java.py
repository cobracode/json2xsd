# coding: utf-8
# Meant to be run with Python 3
import json

INDENT = 2*' '



def getJson(filename):
    print('Reading JSON from file: %s' % filename)
    return json.load(open(filename))

    
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
    
    outputFile.write('%s<xs:complexType name="%s">\n' % (INDENT, className))
    outputFile.write('%s<xs:sequence>\n' % (2*INDENT))
    
    # Write each element (class attribute)
    for element in classDict.keys():
        writeElement(outputFile, element, classDict[element])
    
    outputFile.write('%s</xs:sequence>\n' % (2*INDENT))
    outputFile.write('%s</xs:complexType>\n' % INDENT)
        
    
    
def writeElement(outputFile, elementName, elementDict):
    print('Writing element: %s' % elementName)
    
    
    
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


# import logging
# import os
# import subprocess

# # Define environment variable names
# MUSIC_DIR_VAR = 'MUSIC'

# # Misc
# LOG_FILE = 'getSongs.log'
# SONG_FILE = 'songs.txt'

# MUSIC_DIR = ''
# YMP3 = 'youtube-dl -w --no-post-overwrites --extract-audio --audio-format mp3 --no-mtime -i -o '
# YUPDATE = 'sudo youtube-dl -U'


# def getEnvVars():
  # global MUSIC_DIR
  
  # try:
    # MUSIC_DIR = os.environ[MUSIC_DIR_VAR]
    # logging.debug('Env ' + MUSIC_DIR_VAR + ': \'' + MUSIC_DIR + '\'')
  # except KeyError as e:
    # raise KeyError("Could not get environment variable: %s" % e)
  # except BaseError as e:
    # raise BaseError("Unexpected error while getting environment variables: %s" % e)