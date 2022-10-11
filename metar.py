from typing import List
import requests
import xmltodict

format = "xml"
hours = "1.5"

def checkMetar(metarString) -> List:
    metarString = metarString.upper()
    metarString = metarString.replace(" ", "")
    metarList = metarString.split(",")
    for metar in metarList:
        if len(metar) != 4:
            return "invalid"
    return metarList

def requestMetar(metarList):
    payload = {"datasource":"metars", "requestType": "retrieve", "format": format, "mostRecentForEachStation": "constraint", "hoursBeforeNow": hours, "stationString": ",".join(metarList)}
    request = requests.get("https://www.aviationweather.gov/adds/dataserver_current/httpparam", params=payload)
    return request

def printMetar(metarxml):
    metardict = xmltodict.parse(metarxml.text)
    results = int(metardict["response"]["data"]["@num_results"])
    if results < 1:
        print("No results found.")
    elif results == 1:
        print(metardict["response"]["data"]["METAR"]["raw_text"])
    elif results > 1:
        for i in range(results):
            print(metardict["response"]["data"]["METAR"][i]["raw_text"])

def main():
    needInput = True
    metarList = []
    while needInput:
        metarString = input("Enter a 4 digit ICAO. If multiple, separate by a comma.\n")
        metarList = checkMetar(metarString)
        if metarList == "invalid":
            print("INVALID INPUT, TRY AGAIN")
        else:
            needInput = False
            
    metarxml = requestMetar(metarList)
    printMetar(metarxml)

if __name__ == "__main__":
    main()