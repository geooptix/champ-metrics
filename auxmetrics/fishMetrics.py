import logging

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
    if snorkelFish is None and snorkelFishBinned is None and snorkelFishSteelheadBinned is None:
        visitMetrics[metricName] = None
        return

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

    ####logOutput = "Visit {2}: {0}: {1}".format(metricName, count, visitMetrics["VisitID"])
    ####print logOutput
    ####logging.info(logOutput)

    visitMetrics[metricName] = count


def visitFishCountMetrics(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):

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
        if snorkelFish is None and snorkelFishBinned is None and snorkelFishSteelheadBinned is None:
            c[metricName] = None
            continue

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

        ###logOutput = "Visit {3}: ChannelUnit {0} {1}: {2}".format(channelUnitID, metricName, count, c["VisitID"])
        ###print logOutput
        ###logging.info(logOutput)

        c[metricName] = count


def channelUnitFishCountMetrics(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
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
        if snorkelFish is None and snorkelFishBinned is None and snorkelFishSteelheadBinned is None:
            t[metricName] = None
            continue

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

        ##visitLogOutput = "Visit {3}: {0} {1}: {2}".format(tier1, metricName, count, t["VisitID"])
        ##print visitLogOutput
        ##logging.info(visitLogOutput)

        t[metricName] = count


def tier1FishCountMetrics(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
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



def  structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, speciesNames, metricName):
    for t in structureMetrics:
        structure = t["HabitatStructure"]
        if snorkelFish is None and snorkelFishBinned is None and snorkelFishSteelheadBinned is None:
            t[metricName] = None
            continue
        #print json.dumps(channelUnitIDsForTier, indent=4, sort_keys=True)
        snorkelFishJuvinileCount = 0
        snorkelFishBinnedJuvinileCount = 0
        snorkelFishSteelheadBinnedJuvinileCount = 0

        if not isinstance(speciesNames, list):
            speciesNames = [speciesNames]

        if snorkelFish is not None:
            snorkelFishForSpecies = [s for s in snorkelFish["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["HabitatStructure"] == structure]
            snorkelFishJuvinileCount = sum([int(s["value"]["FishCount"]) for s in snorkelFishForSpecies if int(s["value"]["SizeClass"].replace("mm", "").replace(">", "")) <= maxSizeToBeConsideredJuvinile])

        if snorkelFishBinned is not None:
            snorkelFishBinnedForSpecies = [s for s in snorkelFishBinned["values"] if s["value"]["FishSpecies"] in speciesNames and s["value"]["HabitatStructure"] == structure]
            snorkelFishBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to69mm"]) + int(s["value"]["FishCount70to89mm"]) + int(s["value"]["FishCount90to99mm"]) + int(s["value"]["FishCountGT100mm"]) for s in snorkelFishBinnedForSpecies])

        if snorkelFishSteelheadBinned is not None:
            snorkelFishSteelheadBinnedForSpecies = [s for s in snorkelFishSteelheadBinned["values"] if s["value"]["FishSpecies"] in speciesNames  and s["value"]["HabitatStructure"] == structure]
            snorkelFishSteelheadBinnedJuvinileCount = sum([int(s["value"]["FishCountLT50mm"]) + int(s["value"]["FishCount50to79mm"]) + int(s["value"]["FishCount80to129mm"]) + int(s["value"]["FishCount130to199mm"]) + int(s["value"]["FishCount200to249mm"]) for s in snorkelFishSteelheadBinnedForSpecies])

        count = snorkelFishJuvinileCount + snorkelFishBinnedJuvinileCount + snorkelFishSteelheadBinnedJuvinileCount

        #visitLogOutput = "Visit {3}: {0} {1}: {2}".format(structure, metricName, count, t["VisitID"])
        #print visitLogOutput
        #logging.info(visitLogOutput)

        t[metricName] = count


def structureFishCountMetrics(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Chinook", "CountOfChinook")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Coho", "CountOfCoho")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Sockeye", "CountOfSockeye")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "O. mykiss", "CountOfOmykiss")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Pink", "CountOfPink")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Cutthroat", "CountOfCutthroat")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Bulltrout", "CountOfBulltrout")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Brooktrout", "CountOfBrooktrout")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, "Lamprey", "CountOfLamprey")
    structureFishCountMetricsForSpecies(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, otherSpecies, "CountOfOtherSpecies")


