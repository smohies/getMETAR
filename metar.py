import requests
import xmltodict

hours = "1.5"

# Receives a string of 4 character ICAOs separated by commas. Returns a list of ICAOs.
def transformIcao(icaoString) -> list:
    icaoString = icaoString.upper().replace(" ", "")
    icaoList = icaoString.split(",")
    for icao in icaoList:
        if len(icao) != 4 or not icao.isalnum():
            return "invalid"
    return icaoList

# Receives a list of ICAOs. Returns a METAR XML string.
def requestMetar(icaoList):
    payload = {
        "datasource":"metars", "requestType": "retrieve", "format": "xml",
        "mostRecentForEachStation": "constraint", "hoursBeforeNow": hours,
        "stationString": ",".join(icaoList)
        }
    request = requests.get(
        "https://www.aviationweather.gov/adds/dataserver_current/httpparam",
        params=payload
        )
    if request.status_code == 200:
        return request.text
    else:
        raise Exception(f"Error Code {request.status_code}")

# Receives a METAR XML string. Returns a list with each ICAO raw METAR data.
def getRawMetar(metarXML):
    metarDict = xmltodict.parse(metarXML)
    data = metarDict["response"]["data"]
    results = int(data["@num_results"])
    if results < 1:
        return ["No results found."]
    elif results == 1:
        return [data["METAR"]["raw_text"]]
    elif results > 1:
        raws = []
        for i in range(results):
            raws.append(data["METAR"][i]["raw_text"])
        return raws

def main():
    needInput = True
    icaoList = []
    while needInput:
        icaoString = input(
            "Enter a 4 digit ICAO. If multiple, separate them by a comma.\n"
            )
        icaoList = transformIcao(icaoString)
        if icaoList == "invalid":
            print("INVALID INPUT, TRY AGAIN")
        else:
            needInput = False
            
    metarXML = requestMetar(icaoList)
    rawMetar = getRawMetar(metarXML)
    for each in rawMetar:
        print(each)

if __name__ == "__main__":
    main()