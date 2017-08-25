
import os
import argparse
import json
import ConfigParser
import datetime

from azure.storage.blob import BlockBlobService

from auxmetrics.auxMetrics import processMetrics
from auxmetrics.fishMetrics import *
from sitka_api import *

def main():
    """

    """

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                #if dict1[option] == -1:
                #    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    parser = argparse.ArgumentParser()

    parser.add_argument('logFile', help='Path to output log file', type=str)
    parser.add_argument('visitID', help='Visit ID', type=int, nargs='+')
    args = parser.parse_args()

    if not args.visitID:
        print "ERROR: Missing arguments"
        parser.print_help()
        exit(1)

    # Config setup
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    credentialsSection = ConfigSectionMap("credentials")
    clientID = credentialsSection["clientid"]
    clientSecret = credentialsSection["clientsecret"]
    username = credentialsSection["username"]
    password = credentialsSection["password"]

    apiSection = ConfigSectionMap("api")
    tokenUrl = apiSection["tokenurl"]
    baseApiUrl = apiSection["baseapiurl"]

    azureSection = ConfigSectionMap("azure")
    azureAccount = azureSection["account"]
    azureKey = azureSection["key"]

    outputDirectory = 'output'

    # create a subdirectory to store the metrics in
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    logging.basicConfig(filename=args.logFile, level=logging.INFO, filemode='w')

    # Api setup
    tokenizer = Tokenator.Tokenator(tokenUrl,clientID,clientSecret,username,password)
    apiHelper = ApiHelper.ApiHelper(baseApiUrl, tokenizer.TOKEN)

    # Azure blob setup
    datestring = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    container_name = 'geooptix-container-' + datestring

    block_blob_service = BlockBlobService(account_name=azureAccount, account_key=azureKey)

    # The same containers can hold all types of blobs
    block_blob_service.create_container(container_name)

    for visit_id in args.visitID:
        visit = apiHelper.getVisit(visit_id)

        if visit is None:
            logging.error("Visit was not found for id: {0}".format(visit_id))
            print "Visit was not found for id: {0}".format(visit_id)
            continue

        processVisit(apiHelper, block_blob_service, container_name, visit, visit_id, outputDirectory)

    block_blob_service.create_blob_from_path(container_name, args.logFile, args.logFile)


def processVisit(apiHelper, block_blob_service, container_name, visit, visit_id, outputDirectory):
    protocol = visit["protocol"]
    iteration = str(visit["iterationID"] + 2010)

    infoLog("Visit " + str(visit_id) + " - " + protocol + ": " + iteration)

    visitJsonFile = 'Visit.json'
    with open(visitJsonFile, 'w') as outfile:
        json.dump(visit, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    snorkelFishFile = getMeasurementFile(apiHelper, visit_id, "Snorkel Fish")
    snorkelFishBinnedFile = getMeasurementFile(apiHelper, visit_id, "Snorkel Fish Count Binned")
    snorkelFishSteelheadBinnedFile = getMeasurementFile(apiHelper, visit_id, "Snorkel Fish Count Steelhead Binned")
    channelUnitFile = getMeasurementFile(apiHelper, visit_id, "Channel Unit")
    largeWoodyPieceJsonFile = getMeasurementFile(apiHelper, visit_id, "Large Woody Piece")
    largeWoodyDebrisJsonFile = getMeasurementFile(apiHelper, visit_id, "Large Woody Debris")
    woodyDebrisJamJsonFile = getMeasurementFile(apiHelper, visit_id, "Woody Debris Jam")
    jamHasChannelUnitJsonFile = getMeasurementFile(apiHelper, visit_id, "Jam Has Channel Unit")
    riparianStructureJsonFile = getMeasurementFile(apiHelper, visit_id, "Riparian Structure")
    pebbleJsonFile = getMeasurementFile(apiHelper, visit_id, "Pebble")
    pebbleCrossSectionJsonFile = getMeasurementFile(apiHelper, visit_id, "Pebble Cross-Section")
    channelConstraintJsonFile = getMeasurementFile(apiHelper, visit_id, "Channel Constraints")
    channelConstraintMeasurementJsonFile = getMeasurementFile(apiHelper, visit_id, "Channel Constraint Measurements")
    bankfullWidthJsonFile = getMeasurementFile(apiHelper, visit_id, "Bankfull Width")
    driftInvertJsonFile = getMeasurementFile(apiHelper, visit_id, "Drift Invertebrate Sample")
    driftInvertResultJsonFile = getMeasurementFile(apiHelper, visit_id, "Drift Invertebrate Sample Results")
    sampleBiomassesJsonFile = getMeasurementFile(apiHelper, visit_id, "Sample Biomasses")
    undercutBanksJsonFile = getMeasurementFile(apiHelper, visit_id, "Undercut Banks")
    solarInputMeasurementsJsonFile = getMeasurementFile(apiHelper, visit_id, "Daily Solar Access Meas")
    dischargeJsonFile = getMeasurementFile(apiHelper, visit_id, "Discharge")
    waterChemistryJsonFile = getMeasurementFile(apiHelper, visit_id, "Water Chemistry")
    poolTailFinesJsonFile = getMeasurementFile(apiHelper, visit_id, "Pool Tail Fines")

    fileTuple = processMetrics(visit_id, outputDirectory, visitJsonFile, channelUnitFile, snorkelFishFile, snorkelFishBinnedFile,
                               snorkelFishSteelheadBinnedFile, largeWoodyPieceJsonFile, largeWoodyDebrisJsonFile,
                               woodyDebrisJamJsonFile, jamHasChannelUnitJsonFile, riparianStructureJsonFile, pebbleJsonFile,
                               pebbleCrossSectionJsonFile, channelConstraintJsonFile, channelConstraintMeasurementJsonFile,
                               bankfullWidthJsonFile, driftInvertJsonFile, driftInvertResultJsonFile, sampleBiomassesJsonFile,
                               undercutBanksJsonFile, waterChemistryJsonFile, solarInputMeasurementsJsonFile, dischargeJsonFile,
                               poolTailFinesJsonFile)

    infoLog("Writing Metrics for Visit {0} to Azure Blob storage".format(visit_id))

    #block_blob_service.create_blob_from_path(container_name, "visit_{0}/visit_metrics.json".format(visit_id), fileTuple[0])
    #block_blob_service.create_blob_from_path(container_name, "visit_{0}/channel_unit_metrics.json".format(visit_id), fileTuple[1])
    #block_blob_service.create_blob_from_path(container_name, "visit_{0}/tier1_metrics.json".format(visit_id), fileTuple[2])
    #block_blob_service.create_blob_from_path(container_name, "visit_{0}/structure_metrics.json".format(visit_id), fileTuple[3])



def getMeasurementFile(apiHelper, visit_id, measurement):
    meas = apiHelper.getVisitMeasurements(visit_id, measurement)
    visit_file = '{0}.json'.format(measurement)
    with open(visit_file, 'w') as outfile:
        json.dump(meas, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    return visit_file


def infoLog(message):
    logging.info(message)
    print message


if __name__ == "__main__":
    main()