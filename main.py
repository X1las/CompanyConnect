import json
from classes import Source, Pair, Logger

data = json.load(open('CasaAS.json'))
pairs: Pair = []
sources: Source = []
log = Logger(priority=2)

for i in data:

    tempSID = str(i["source"])
    tempTID = str(i["target"])
    tempSource = None
    tempTarget = None

    sExists = False
    tExists = False

    for x in sources:
        if x.id == tempSID:
            sExists = True
            tempSource = x
        elif x.id == tempTID:
            tExists = True
            tempTarget = x
        elif tExists and sExists:
            break

    if not sExists:
        sources.append(
            Source(tempSID, log, name=i["source_name"], debth=i["source_depth"]))
        tempSource = sources[len(sources)-1]
    if not tExists:
        sources.append(
            Source(tempTID, log, name=i["target_name"], debth=i["target_depth"]))
        tempTarget = sources[len(sources)-1]

    txt = i["share"].replace("%", "")
    x = txt.split("-")

    temp_average, temp_upper, temp_lower = x[0], x[0], x[0]

    if not int(i["target_depth"]) < int(i["source_depth"]):
        print("here!")

    if(len(x) > 1):

        temp_average = (float(x[0])+float(x[1]))/2
        temp_upper = x[1]
        temp_lower = x[0]
    elif(x[0][0] == "<"):
        temp_average = "2.5"
        temp_upper = "5"
        temp_lower = "0"

    tempPair = Pair(tempSource, tempTarget, log, average=float(
        temp_average), real_up=float(temp_upper), real_down=float(temp_lower))
    pairs.append(tempPair)
    tempSource.pairs.append(tempPair)

for i in sources:
    if i.name == "CASA A/S":
        i.search("39641208")
