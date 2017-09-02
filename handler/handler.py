# -*- coding: utf-8 -*- 
#!/usr/bin/python
import string
import os
from dictdiffer import diff, patch, swap, revert


aFilePath = 'o2lji1mtas100.ldif'
bFilePath = 'o2lji1mtas200.ldif'
outputFilePath = 'output.csv'
filterList = ["objectClass",
              "ownerId",
              "groupId",
              "shareTree",
              "permissions",
              "#"
              ]


def filterOut(inputString,listToFilterOut):
    inputStringList = inputString.split("\n")
    outputString = str()
    for line in inputStringList:
        if not any(filterWord in line for filterWord in listToFilterOut):
            outputString = outputString + "\n" + line
    return outputString

def parseLDIF(inputFilePath):
    inputString = str()
    with open(inputFilePath) as inputFile:
        inputString = inputFile.read().strip()
        inputStringFiltered = filterOut(inputString,filterList)
        inputInDn = inputStringFiltered.split("dn:")
    nodeInformation = inputInDn[1]

    dnTable = dict()
    for dn in inputInDn[2:]:
        keyAndValue = dn.strip().split("\n") 
        key = keyAndValue[0].split(",nodeName")[0]
        value = ", ".join(keyAndValue[1:])
        dnTable[key] = value
    output = dict()
    output["nodeInformation"] = nodeInformation
    output["dnTable"] = dnTable
    return output

aParsedFile = parseLDIF(aFilePath)
bParsedFile = parseLDIF(bFilePath)

compareResult = list(diff(aParsedFile["dnTable"], bParsedFile["dnTable"]))

outputCSV =                     "result"     + "," + "dn"                  + "," + aFilePath               + "," + bFilePath

def removeComma(input):
    return input.replace(",","|")

for line in compareResult:
    if line[0] == "change":
        appendLine     = "\n" + "diff"       + "," + removeComma(line[1])  + "," + removeComma(line[2][0]) + "," + removeComma(line[2][1])
    outputCSV = outputCSV + appendLine
    if line[0] == "add":
        for item in line[2]:
            appendLine = "\n" + "leftMiss"   + "," + removeComma(item[0])  + "," + "NOTHING HERE"          + "," + removeComma(item[1]) 
            outputCSV = outputCSV + appendLine
    if line[0] == "remove":
        for item in line[2]:
            appendLine = "\n" + "rightMiss"  + "," + removeComma(item[0])  + "," + removeComma(item[1])    + "," + "NOTHING HERE"          
            outputCSV = outputCSV + appendLine


with open(outputFilePath,'w') as outputFileP:
    outputFileP.write(outputCSV)


'''
filter out:
    objectClass: NumAnaLocalCallTable
    ownerId: 0
    groupId: 0
    shareTree: nodeName=22bti1mtas000
    permissions: 15
    nodeName
'''