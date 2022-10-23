import requests
import xmltodict
from tkinter import *
from tkinter.ttk import *

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
        "mostRecentForEachStation": "constraint", "hoursBeforeNow": "2",
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
    if results == 1:
        return [data["METAR"]["raw_text"]]
    if results > 1:
        raws = []
        for i in range(results):
            raws.append(data["METAR"][i]["raw_text"])
        return raws

# App logic
def app_request():
    txt_metar.delete("1.0", END)
    entry = ent_entry.get()
    icao_list = transformIcao(entry)
    if icao_list == "invalid":
        txt_metar.insert("1.0", "Invalid ICAO format, try again.")
    else:
        metar_xml = requestMetar(icao_list)
        metar_raw = getRawMetar(metar_xml)
        txt_metar.insert("1.0", "\n".join(metar_raw))


# Tkinter GUI
window = Tk()
window.title("getMETAR")
window.resizable(width=False, height=False)

lbl_entry = Label(master=window, text="Input a valid 4 character ICAO code. If multiple, separate them with commas.")
ent_entry = Entry(master=window, width=50)
btn_request = Button(master=window, text="REQUEST METAR", command=app_request)
txt_metar = Text(master=window, width=120, height=15)

lbl_entry.grid(columnspan=2, row=0, pady=10)
ent_entry.grid(column=0, row=1, sticky="e", padx=5)
btn_request.grid(column=1, row=1, sticky="w", padx=5)
txt_metar.grid(columnspan=2, row=2, pady=10, padx=10)

window.mainloop()