import requests
import xmltodict

hours = "1.5"

def transformMetar(metarString) -> list:
    metarString = metarString.upper()
    metarString = metarString.replace(" ", "")
    metarList = metarString.split(",")
    for metar in metarList:
        if len(metar) != 4:
            return "invalid"
    return metarList

def requestMetar(metarList):
    payload = {
        "datasource":"metars", "requestType": "retrieve", "format": "xml",
        "mostRecentForEachStation": "constraint", "hoursBeforeNow": hours,
        "stationString": ",".join(metarList)
        }
    request = requests.get(
        "https://www.aviationweather.gov/adds/dataserver_current/httpparam",
        params=payload)
    return request

def printMetar(metarXML):
    metarDict = xmltodict.parse(metarXML.text)
    data = metarDict["response"]["data"]
    results = int(data ["@num_results"])
    if results < 1:
        print("No results found.")
    elif results == 1:
        print(data ["METAR"]["raw_text"])
    elif results > 1:
        for i in range(results):
            print(data ["METAR"][i]["raw_text"])

def main():
    needInput = True
    metarList = []
    while needInput:
        metarString = input(
            "Enter a 4 digit ICAO. If multiple, separate by a comma.\n"
            )
        metarList = transformMetar(metarString)
        if metarList == "invalid":
            print("INVALID INPUT, TRY AGAIN")
        else:
            needInput = False
            
    metarXML = requestMetar(metarList)
    printMetar(metarXML)

if __name__ == "__main__":
    main()