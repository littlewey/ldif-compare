# -*- coding: utf-8 -*- 
#!env/bin/python
import string
import os
from dictdiffer import diff, patch, swap, revert
from config import filterList

from flask_table import Table, Col

'''
TEST local File

aFilePath = 'o2lji1mtas100.ldif'
bFilePath = 'o2lji1mtas200.ldif'
aFile = open('aFilePath', 'r')
bFile = open('bFilePath', 'r')
TEST local File End
'''



outputFilePath = 'output.csv'

def filterOut(inputString,listToFilterOut):
    inputStringList = inputString.split("\n")
    outputString = str()
    for line in inputStringList:
        if not any(filterWord in line for filterWord in listToFilterOut):
            outputString = outputString + "\n" + line
    return outputString
def parseLDIF(inputFile):
    inputString = inputFile.read().strip()
    inputStringFiltered = filterOut(inputString,filterList)
    inputInDn = inputStringFiltered.split("dn:")
    nodeInformation = inputInDn[1]
    dnTable = dict()
    for dn in inputInDn[2:]:
        keyAndValue = dn.strip().split("\n") 
        # Remove nodeName
        key = keyAndValue[0].split(",nodeName")[0]
        value = ", ".join(keyAndValue[1:])
        dnTable[key] = value
    '''
    output is a dict with key :
                               "nodeInformation"
                               "dnTable"
    '''
    output = dict()
    output["nodeInformation"] = nodeInformation
    output["dnTable"] = dnTable
    return output

def removeComma(input):
    '''
    remove Comma to enable csv files' column correctly parsed by fucking M$ Excel
    '''
    return input.replace(",","|")

def commaAddNewline(input):
    '''
    remove Comma to enable csv files' column correctly parsed by fucking M$ Excel
    '''
    return input.replace(",",",\n")

def buildResultRow(result,dn,aFileValue,bFileValue):
    return [result,dn,aFileValue,bFileValue]
def buildCsvLine(resultRow):
    return "\n" + ",".join([removeComma(x) for x in resultRow])
def buildTableItem(resultRow):
    return dict(result = commaAddNewline(resultRow[0]),
                dn     = commaAddNewline(resultRow[1]),
                aFileValue = commaAddNewline(resultRow[2]),
                bFileValue = commaAddNewline(resultRow[3])
                )

def ldifCompareHandler(aFile,bFile):
    '''
    parsedFile as below are in structure dict, see details in function parseLDIF
    '''
    aParsedFile = parseLDIF(aFile)
    bParsedFile = parseLDIF(bFile)

    compareResult = list(diff(aParsedFile["dnTable"], bParsedFile["dnTable"]))
    '''
    Build CSV file Header, which is actually the first line
    '''
    outputCSV =                     "result"     + "," + "dn"                  + "," + "first File"            + "," + "second File"

    '''
    Build items = [] for render table
    '''
    items = []
    for line in compareResult:
        if line[0] == "change":
            row = buildResultRow("diff",str(line[1]),str(line[2][0]),str(line[2][1]) )
            appendLine = buildCsvLine(row)
            appendItem = buildTableItem(row)
            outputCSV = outputCSV + appendLine
            items.append(appendItem)
        if line[0] == "add":
            for item in line[2]:
                row = buildResultRow("leftMiss",str(item[0]) ,"NOTHING HERE",str(item[1]) )
                appendLine = buildCsvLine(row)
                appendItem = buildTableItem(row)
                outputCSV = outputCSV + appendLine
                items.append(appendItem)
        if line[0] == "remove":
            for item in line[2]:
                row = buildResultRow("rightMiss",str(item[0]) ,str(item[1]),"NOTHING HERE")
                appendLine = buildCsvLine(row)
                appendItem = buildTableItem(row)
                outputCSV = outputCSV + appendLine
                items.append(appendItem)

    '''
    TEST
    with open(outputFilePath,'w') as outputFileP:
        outputFileP.write(outputCSV)
    TEST END
    '''
    return items

