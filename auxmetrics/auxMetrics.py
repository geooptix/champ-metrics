import json

from auxmetrics.metricUtil import populateDefaultColumns

from auxmetrics.fishMetrics import *
from auxmetrics.woodMetrics import *
from auxmetrics.coverMetrics import *


def calculateMetricsForVisit(visitid, visit, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits, riparianStructures):

    visitMetrics = dict()
    populateDefaultColumns(visitMetrics, visitid)

    visitFishCountMetrics(visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
    visitLWDMetrics(visitMetrics, visit, channelUnits, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits)
    visitCoverMetrics(visitMetrics, visit, riparianStructures)
    return visitMetrics

def calculateMetricsForChannelUnitSummary(visitid, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces):

    channelUnitMetrics = []
    # create the channel unit summary metric rows with the channel unit id

    if channelUnits is not None:
        for c in channelUnits["values"]:
            cu = dict()
            cu["ChannelUnitID"] = c["value"]["ChannelUnitID"]
            populateDefaultColumns(cu, visitid)
            channelUnitMetrics.append(cu)

        channelUnitFishCountMetrics(channelUnitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
        channelUnitLWDMetrics(channelUnitMetrics, largeWoodyPieces)

    return channelUnitMetrics

def calculateMetricsForTier1Summary(visitid, visit, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits):

    tier1Metrics = []
    # create the tier 1 summary metric rows with the correct tier 1
    if channelUnits is not None:
        tier1s = [t["value"]["Tier1"] for t in channelUnits["values"]]
        tier1s = list(set(tier1s))  # this is a quick distinct

        for c in tier1s:
            t = dict()
            t["Tier1"] = c
            populateDefaultColumns(t, visitid)
            tier1Metrics.append(t)

        tier1FishCountMetrics(tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
        tier1LWDMetrics(tier1Metrics, visit, channelUnits, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits)

    return tier1Metrics

def calculateMetricsForStructureSummary(visitid, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned):

    structureMetrics = []
    # create the correct structure type metric summaries
    structures = []

    if snorkelFish is not None:
        structures.extend([t["value"]["HabitatStructure"] for t in snorkelFish["values"]])
    if snorkelFishBinned is not None:
        structures.extend([t["value"]["HabitatStructure"] for t in snorkelFishBinned["values"]])
    if snorkelFishSteelheadBinned is not None:
        structures.extend([t["value"]["HabitatStructure"] for t in snorkelFishSteelheadBinned["values"]])

    st = list(set(structures))

    for c in st:
        t = dict()
        t["HabitatStructure"] = c
        populateDefaultColumns(t, visitid)
        structureMetrics.append(t)

    structureFishCountMetrics(structureMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)

    return structureMetrics

def loadJsonFile(jsonFilePath):
    if jsonFilePath == None:
        return None

    with open(jsonFilePath) as data_file:
        data = json.load(data_file)
        return data

def processMetrics(visitid, outputDirectory, visitJsonFile, channelUnitJsonFile, snorkelFishJsonFile, snorkelFishBinnedJsonFile, snorkelFishSteelheadBinnedJsonFile, largeWoodyPieceJsonFile, largeWoodyDebrisJsonFile, woodyDebrisJamJsonFile, jamHasChannelUnitJsonFile, riparianStructureJsonFile):
    #only load json for files that didn't return 404s
    visit = loadJsonFile(visitJsonFile)
    snorkelFish = loadJsonFile(snorkelFishJsonFile)
    snorkelFishBinned = loadJsonFile(snorkelFishBinnedJsonFile)
    snorkelFishSteelheadBinned = loadJsonFile(snorkelFishSteelheadBinnedJsonFile)
    channelUnits = loadJsonFile(channelUnitJsonFile)
    largeWoodyPieces = loadJsonFile(largeWoodyPieceJsonFile)
    largeWoodyDebris = loadJsonFile(largeWoodyDebrisJsonFile)
    woodyDebrisJams = loadJsonFile(woodyDebrisJamJsonFile)
    jamHasChannelUnits = loadJsonFile(jamHasChannelUnitJsonFile)
    riparianStructures = loadJsonFile(riparianStructureJsonFile)

    #do metric calcs
    visitMetrics = calculateMetricsForVisit(visitid, visit, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits, riparianStructures)
    channelUnitMetrics = calculateMetricsForChannelUnitSummary(visitid, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces)
    tier1Metrics = calculateMetricsForTier1Summary(visitid, visit, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned, largeWoodyPieces, largeWoodyDebris, woodyDebrisJams, jamHasChannelUnits)
    structureMetrics = calculateMetricsForStructureSummary(visitid, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)

    #write these files

    # print json.dumps(tier1Metrics, indent=4, sort_keys=True)
    tier1_json_file_path = "{0}/visit_{1}_tier1Metrics.json".format(outputDirectory, visitid)
    with open(tier1_json_file_path, 'w') as outfile:
        json.dump(tier1Metrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    # print json.dumps(tier1Metrics, indent=4, sort_keys=True)
    structure_json_file_path = "{0}/visit_{1}_structureMetrics.json".format(outputDirectory, visitid)
    with open(structure_json_file_path, 'w') as outfile:
        json.dump(structureMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    # print json.dumps(channelUnitMetrics, indent=4, sort_keys=True)
    channel_unit_json_file_path = "{0}/visit_{1}_channelUnitMetrics.json".format(outputDirectory, visitid)
    with open(channel_unit_json_file_path, 'w') as outfile:
        json.dump(channelUnitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    # print json.dumps(visitMetrics, indent=4, sort_keys=True)
    visit_json_file_path = "{0}/visit_{1}_Metrics.json".format(outputDirectory, visitid)
    with open(visit_json_file_path, 'w') as outfile:
        json.dump(visitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    return (visit_json_file_path, channel_unit_json_file_path, tier1_json_file_path, structure_json_file_path)