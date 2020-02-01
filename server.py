from flask import Flask, render_template
import json


#methods
def getJsonDataFromFile():
    insaFile = open("C:\\Users\\Robin\\Google Drive\\Privat\\IONOS\\Sonntagsfrage-Website\\data\\insa.json")
    jsonData = json.load(insaFile)
    return cleanJsonData(jsonData)

def cleanJsonData(jsonData:map):
    newJsonData:dict = {}
    newJsonData["parties"] = jsonData["parties"]
    newJsonData["values"] = {}
    for item in jsonData["values"].items():
        timestamp = item[0]
        values:list = item[1]
        newValues:list = []
        for value in values:
            # remove % and replace "," by "." ("12,5%" ==> "12.5")
            newValues.append(percentageStrToInt(value))
        #print(newValues)
        newJsonData["values"][timestamp] = newValues
        
    return newJsonData

def percentageStrToInt(s:str):
    s = s[:-2].replace(",",".")
    try:
        return float(s)
    except:
        return float(0)
    

def getParties(valueMap:map):
    return valueMap["parties"]

def reverse(l:list):
    l.reverse()
    return l

def getValuesSorted(valueMap:map, index:int):
    s:str = "25.09.2012"
    keysSorted = getKeysSorted(valueMap)
    values:list = []
    for key in keysSorted:
        percentageValues:list = valueMap["values"][key]
        if (len(percentageValues) > index):
            values.append(percentageValues[index])
        else:
            values.append('')
    return values

def getKeysSorted(valueMap:map):
    return sorted(valueMap["values"].keys(), key=lambda d: '.'.join(reverse(d.split('.'))), reverse=True)

#variables
app = Flask(__name__)

@app.route('/')
def index():
    #return getJsonDataFromFile()
    jsonData = getJsonDataFromFile()
    return render_template('sonntagsfrage.htm', test1="Hallo, test1!", test2="Hallo, test2!", jsonData=jsonData, parties=getParties(jsonData), keysSorted=getKeysSorted(jsonData))

if __name__ == '__main__':
    jsonData = getJsonDataFromFile()
    print(getParties(jsonData))
    print(getValuesSorted(jsonData, 3))
    app.run(debug=True)