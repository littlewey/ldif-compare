# -*- coding: utf-8 -*-
#!env/bin/python
import string
import os
from dictdiffer import diff, patch, swap, revert
from config import filterList
from difflib import Differ

#from flask_table import Table, Col

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
    # avoide # in middle of a line
    inputString = inputString.replace("#","\n#")
    # avoide # in middle of a line
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
    #nodeInformation = inputInDn[1]
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
    #output["nodeInformation"] = nodeInformation
    output["dnTable"] = dnTable
    return output

def removeComma(input):
    '''
    remove Comma to enable csv files' column correctly parsed by fucking M$ Excel
    '''
    return input.replace(",","|")
def addQuotation(input):
    '''
    remove Comma to enable csv files' column correctly parsed by fucking M$ Excel
    '''
    return u'"'+ input + u'"'
def commaAddNewline(input):
    '''
    remove Comma to enable csv files' column correctly parsed by fucking M$ Excel
    '''
    return input.replace(",",",\n")

def buildResultRow(result,dn,aFileValue,bFileValue):
    return [result,dn,aFileValue,bFileValue]
def buildCsvLine(resultRow):
    return "\n" + ",".join([addQuotation(commaAddNewline(x)) for x in resultRow])
def buildTableItem(resultRow):
    return dict(result = commaAddNewline(resultRow[0]),
                dn     = commaAddNewline(resultRow[1]),
                aFileValue = commaAddNewline(resultRow[2]),
                bFileValue = commaAddNewline(resultRow[3])
                )

# compare two values, return diffs

def getDeltaValue(valueA, valueB):
    valueA = valueA + ","
    valueB = valueB + ","
    diffMarkList = list(Differ().compare(valueA, valueB))
    # test print str(diffMarkList)
    deltaValueA = str()
    deltaValueB = str()
    propertyA = str()
    propertyB = str()
    deltaFlag = False
    for eachChar in diffMarkList:
        # eachChar[-1] is the current char
        # eachChar[:1] is the diff mark, + means value from A, - means value from B, space means common part
        if eachChar[-1] == ",":
            if deltaFlag:
                # fixing bugs that add a comma even when propertyA or *B is ""
                deltaValueA = (deltaValueA + propertyA + ",") if propertyA else deltaValueA
                deltaValueB = (deltaValueB + propertyB + ",") if propertyB else deltaValueB
            propertyA = ""
            propertyB = ""
            deltaFlag = False
        else:
            diffState   = eachChar[:1]
            currentChar = eachChar[-1]
            if diffState == " ":
                propertyA = propertyA + currentChar
                propertyB = propertyB + currentChar
            if diffState == "+":
                propertyA = propertyA + currentChar
                deltaFlag = True
            if diffState == "-":
                propertyB = propertyB + currentChar
                deltaFlag = True
    return dict(A = deltaValueA, B = deltaValueB )


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
    outputCSV = "result" + "," + "dn without nodename" + "," + "Value in 1st File" + "," + "Value in 2nd File"

    '''
    Build items = [] for render table
    '''
    # items for jinja2 html table
    items = []
    # data for slicGrid
    data = [["Result","DN","Value of 1st File","Value of 2nd File"]]
    for line in compareResult:
        if line[0] == "change":
            # improved result in values, show only delta part
            valueA = str(line[2][0])
            #print "valueA" + valueA
            valueB = str(line[2][1])
            #print "valueB" + valueB
            diffValue = getDeltaValue(valueA,valueB)
            # improved result in values, show only delta part

            row = buildResultRow("diff",str(line[1]),diffValue["A"], diffValue["B"])
            appendLine = buildCsvLine(row)
            appendItem = buildTableItem(row)
            outputCSV = outputCSV + appendLine
            items.append(appendItem)
            data.append([commaAddNewline(eachCell) for eachCell in row])
        if line[0] == "add":
            for item in line[2]:
                row = buildResultRow("leftMiss",str(item[0]) ,"NOTHING HERE",str(item[1]) )
                appendLine = buildCsvLine(row)
                appendItem = buildTableItem(row)
                outputCSV = outputCSV + appendLine
                items.append(appendItem)
                data.append([commaAddNewline(eachCell) for eachCell in row])
        if line[0] == "remove":
            for item in line[2]:
                row = buildResultRow("rightMiss",str(item[0]) ,str(item[1]),"NOTHING HERE")
                appendLine = buildCsvLine(row)
                appendItem = buildTableItem(row)
                outputCSV = outputCSV + appendLine
                items.append(appendItem)
                data.append([commaAddNewline(eachCell) for eachCell in row])

    '''
    TEST
    with open(outputFilePath,'w') as outputFileP:
        outputFileP.write(outputCSV)
    TEST END
    '''
    output = {"table":items , "csv":outputCSV, "data":data}
    return output

