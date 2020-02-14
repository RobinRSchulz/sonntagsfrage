from flask import Flask, render_template
import json, os, sched, time, threading
import getData


# data stuff todo:
datagettingScheduler = sched.scheduler(time.time, time.sleep)
dataGettingThread = None

def dataGettingEvent(sc):
    print("Fetching data")
    getData.main()

    #re-setup scheduler
    # todo set this way higher
    datagettingScheduler.enter(180, 1, dataGettingEvent, (sc,))

def dataGettingThreadEntry():
    datagettingScheduler.enter(60, 1, dataGettingEvent, (datagettingScheduler,))
    datagettingScheduler.run()

def setupDataGettingEvent():
    dataGettingThread = threading.Thread(target=dataGettingThreadEntry)
    dataGettingThread.start()
    
    


#methods
def getJsonDataFromFile(institue_id:str):
    insaFile = open(os.path.join(getDataLocation(), institue_id, ".json"))

    jsonData = json.load(insaFile)
    return cleanJsonData(jsonData)

def getDataLocation():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

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
    jsonData = getJsonDataFromFile("insa")
    return render_template('index.htm', test1="Hallo, test1!", test2="Hallo, test2!", )

@app.route('/institute/<institute_id>')
def institute(institute_id):
    jsonData = getJsonDataFromFile(institute_id)
    return render_template('sonntagsfrage.htm', test1="Hallo, test1!", test2="Hallo, test2!", jsonData=jsonData, parties=getParties(jsonData), keysSorted=getKeysSorted(jsonData), instituteId=institute_id)

if __name__ == '__main__':
    #jsonData = getJsonDataFromFile("insa")
    #print(getParties(jsonData))
    #print(getValuesSorted(jsonData, 3))
    print('Setting up data getting event')
    setupDataGettingEvent()
    print('Starting server.')
    app.run(host="0.0.0.0", port=int("8080"), debug=True)
