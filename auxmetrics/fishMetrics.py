import logging
import datetime

__version__ = '0.1.0'

maxSizeToBeConsideredJuvinile = 250

otherSpecies = [
    "Chum",
    "Sucker",
    "Mountain White Fish",
    "Rainbow",
    "Sculpin",
    "Cyprinids",
    "Stickleback",
    "Other",
    "Unknown",
    "Dace Species",
    "Sunfish",
    "Unknown Salmon",
    "Tailed Frog",
    "Tailed Frog Tadpole",
    "Pacific Giant Salamander"
]


def visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, speciesNames, metricName):
    snorkelFishJuvinileCount = 0
    snorkelFishBinnedJuvinileCount = 0
    snorkelFishSteelheadBinnedJuvinileCount = 0

    if not isinstance(speciesNames, list):
        speciesNames = [speciesNames]

    if snorkelFish is not None:
        snorkelFishForSpecies = [s for s in snorkelFish["values"] if s["value"]["FishSpecies"] in speciesNames]
        snorkelFishJuvinileCount = sum([int(s["value"]["FishCount"]) for s in snorkelFishForSpecies if int(s["value"]["SizeClass"].replace("mm", "").replace(">", "")) <= maxSizeToBeConsideredJuvinile])

    if snorkelFishBinned is not None:
        snorkelFishBinnedForSpecies = [s for s in snorkelFishBinned["values"] if s["value"]["FishSpecies"] in speciesNames]
        snorkelFishBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to69mm"]) + int(s["value"]["FishCount70to89mm"]) + int(s["value"]["FishCount90to99mm"]) + int(s["value"]["FishCountGT100mm"]) for s in snorkelFishBinnedForSpecies])

    if snorkelFishSteelheadBinned is not None:
        snorkelFishSteelheadBinnedForSpecies = [s for s in snorkelFishSteelheadBinned["values"] if s["value"]["FishSpecies"] in speciesNames]
        snorkelFishSteelheadBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to79mm"]) + int(s["value"]["FishCount80to129mm"]) + int(s["value"]["FishCount130to199mm"]) + int(s["value"]["FishCount200to249mm"]) for s in snorkelFishSteelheadBinnedForSpecies ])

    count = snorkelFishJuvinileCount + snorkelFishBinnedJuvinileCount + snorkelFishSteelheadBinnedJuvinileCount

    logOutput = "Visit {2}: {0}: {1}".format(metricName, count, visitMetrics["VisitID"])
    print logOutput
    logging.info(logOutput)

    visitMetrics[metricName] = count


def visitFishCountMetrics(visitid, visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
    visitMetrics["VisitID"] = visitid
    visitMetrics["EngineVersion"] = __version__
    visitMetrics["CalcDate"] = datetime.datetime.utcnow().isoformat() + 'Z'
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Chinook", "CountOfChinook")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Coho", "CountOfCoho")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Sockeye", "CountOfSockeye")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "O. mykiss", "CountOfOmykiss")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Pink", "CountOfPink")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Cutthroat", "CountOfCutthroat")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Bulltrout", "CountOfBulltrout")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Brooktrout", "CountOfBrooktrout")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Lamprey", "CountOfLamprey")
    visitFishCountMetricsForSpecies(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, otherSpecies, "CountOfOtherSpecies")


def channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, speciesNames, metricName):
    for c in channelUnitMetrics:
        channelUnitID = c["ChannelUnitID"]

        snorkelFishJuvinileCount = 0
        snorkelFishBinnedJuvinileCount = 0
        snorkelFishSteelheadBinnedJuvinileCount = 0

        if not isinstance(speciesNames, list):
            speciesNames = [speciesNames]

        if snorkelFish is not None:
            snorkelFishForSpecies = [s for s in snorkelFish["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["ChannelUnitID"] == channelUnitID]
            snorkelFishJuvinileCount = sum([int(s["value"]["FishCount"]) for s in snorkelFishForSpecies if int(s["value"]["SizeClass"].replace("mm", "").replace(">", "")) <= maxSizeToBeConsideredJuvinile])

        if snorkelFishBinned is not None:
            snorkelFishBinnedForSpecies = [s for s in snorkelFishBinned["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["ChannelUnitID"] == channelUnitID]
            snorkelFishBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to69mm"]) + int(s["value"]["FishCount70to89mm"]) + int(s["value"]["FishCount90to99mm"]) + int(s["value"]["FishCountGT100mm"]) for s in snorkelFishBinnedForSpecies])

        if snorkelFishSteelheadBinned is not None:
            snorkelFishSteelheadBinnedForSpecies = [s for s in snorkelFishSteelheadBinned["values"] if s["value"]["FishSpecies"] in speciesNames  and s["value"]["ChannelUnitID"] == channelUnitID]
            snorkelFishSteelheadBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to79mm"]) + int(s["value"]["FishCount80to129mm"]) + int(s["value"]["FishCount130to199mm"]) + int(s["value"]["FishCount200to249mm"]) for s in snorkelFishSteelheadBinnedForSpecies])

        count = snorkelFishJuvinileCount + snorkelFishBinnedJuvinileCount + snorkelFishSteelheadBinnedJuvinileCount

        logOutput = "Visit {3}: ChannelUnit {0} {1}: {2}".format(channelUnitID, metricName, count, c["VisitID"])
        print logOutput
        logging.info(logOutput)

        c[metricName] = count


def channelUnitFishCountMetrics(visitid, channelUnitMetrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
    # create the channel unit summary metric rows with the correct channel unit numbers
    for c in channelUnits["values"]:
        cu = dict()
        cu["ChannelUnitID"] = c["value"]["ChannelUnitID"]
        cu["VisitID"] = visitid
        cu["EngineVersion"] = __version__
        cu["CalcDate"] = datetime.datetime.utcnow().isoformat() + 'Z'
        channelUnitMetrics.append(cu)

    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Chinook", "CountOfChinook")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Coho", "CountOfCoho")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Sockeye", "CountOfSockeye")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "O. mykiss", "CountOfOmykiss")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Pink", "CountOfPink")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Cutthroat", "CountOfCutthroat")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Bulltrout", "CountOfBulltrout")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Brooktrout", "CountOfBrooktrout")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Lamprey", "CountOfLamprey")
    channelUnitFishCountMetricsForSpecies(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, otherSpecies, "CountOfOtherSpecies")




def tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, speciesNames, metricName):
    for t in tier1Metrics:
        tier1 = t["Tier1"]
        channelUnitIDsForTier = [c["value"]["ChannelUnitID"] for c in channelUnits["values"] if c["value"]["Tier1"] == tier1]
        #print json.dumps(channelUnitIDsForTier, indent=4, sort_keys=True)
        snorkelFishJuvinileCount = 0
        snorkelFishBinnedJuvinileCount = 0
        snorkelFishSteelheadBinnedJuvinileCount = 0

        if not isinstance(speciesNames, list):
            speciesNames = [speciesNames]

        if snorkelFish is not None:
            snorkelFishForSpecies = [s for s in snorkelFish["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["ChannelUnitID"] in channelUnitIDsForTier]
            snorkelFishJuvinileCount = sum([int(s["value"]["FishCount"]) for s in snorkelFishForSpecies if int(s["value"]["SizeClass"].replace("mm", "").replace(">", "")) <= maxSizeToBeConsideredJuvinile])

        if snorkelFishBinned is not None:
            snorkelFishBinnedForSpecies = [s for s in snorkelFishBinned["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["ChannelUnitID"] in channelUnitIDsForTier]
            snorkelFishBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to69mm"]) + int(s["value"]["FishCount70to89mm"]) + int(s["value"]["FishCount90to99mm"]) + int(s["value"]["FishCountGT100mm"]) for s in snorkelFishBinnedForSpecies])

        if snorkelFishSteelheadBinned is not None:
            snorkelFishSteelheadBinnedForSpecies = [s for s in snorkelFishSteelheadBinned["values"] if s["value"]["FishSpecies"] in speciesNames  and s["value"]["ChannelUnitID"] in channelUnitIDsForTier]
            snorkelFishSteelheadBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to79mm"]) + int(s["value"]["FishCount80to129mm"]) + int(s["value"]["FishCount130to199mm"]) + int(s["value"]["FishCount200to249mm"]) for s in snorkelFishSteelheadBinnedForSpecies])

        count = snorkelFishJuvinileCount + snorkelFishBinnedJuvinileCount + snorkelFishSteelheadBinnedJuvinileCount

        visitLogOutput = "Visit {3}: {0} {1}: {2}".format(tier1, metricName, count, t["VisitID"])
        print visitLogOutput
        logging.info(visitLogOutput)

        t[metricName] = count


def tier1FishCountMetrics(visitid, tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
    # create the tier 1 summary metric rows with the correct tier 1
    tier1s = [t["value"]["Tier1"] for t in channelUnits["values"]]
    tier1s = list(set(tier1s))  # this is a quick distinct

    for c in tier1s:
        t = dict()
        t["Tier1"] = c
        t["VisitID"] = visitid
        t["EngineVersion"] = __version__
        t["CalcDate"] = datetime.datetime.utcnow().isoformat() + 'Z'
        tier1Metrics.append(t)

    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Chinook", "CountOfChinook")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Coho", "CountOfCoho")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Sockeye", "CountOfSockeye")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "O. mykiss", "CountOfOmykiss")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Pink", "CountOfPink")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Cutthroat", "CountOfCutthroat")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Bulltrout", "CountOfBulltrout")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Brooktrout", "CountOfBrooktrout")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Lamprey", "CountOfLamprey")
    tier1FishCountMetricsForSpecies(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, otherSpecies, "CountOfOtherSpecies")
    

def structureFishCountMetrics():
    pass


