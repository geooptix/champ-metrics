
import argparse
import json
import ConfigParser
import datetime

from azure.storage.blob import BlockBlobService

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

    #Config setup
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

    logging.basicConfig(filename=args.logFile, level=logging.INFO, filemode='w')

    #Api setup
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

        processVisit(apiHelper, block_blob_service, container_name, visit, visit_id)

    block_blob_service.create_blob_from_path(container_name, args.logFile, args.logFile)


def processVisit(apiHelper, block_blob_service, container_name, visit, visit_id):
    protocol = visit["protocol"]
    iteration = str(visit["iterationID"] + 2010)

    infoLog("Visit " + str(visit_id) + " - " + protocol + ": " + iteration)

    snorkelFish = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish")
    snorkelFishBinned = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish Count Binned")
    snorkelFishSteelheadBinned = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish Count Steelhead Binned")
    # print "Writing Visit data to file"
    # visit_file = 'data/visit_{}.json'.format(visit_id)
    # with open(visit_file, 'w') as outfile:
    #    json.dump(visit, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    # print json.dumps(snorkelFish, indent=4, sort_keys=True)
    # print json.dumps(snorkelFishBinned, indent=4, sort_keys=True)
    # print json.dumps(snorkelFishSteelheadBinned, indent=4, sort_keys=True)

    visitMetrics = dict()
    infoLog("Calculate Fish Count Metrics for Visit {0}".format(visit_id))
    visitFishCountMetrics(visit_id, visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
    # print json.dumps(visitMetrics, indent=4, sort_keys=True)
    visitJsonFilePath = "data/visit_{0}_fishCounts.json".format(visit_id)
    with open(visitJsonFilePath, 'w') as outfile:
        json.dump(visitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    channelUnits = apiHelper.getVisitMeasurements(visit_id, "Channel Unit")
    channelUnitMetrics = []
    infoLog("Calculate Fish Count Metrics for Channel Units for Visit {0}".format(visit_id))
    channelUnitFishCountMetrics(visit_id, channelUnitMetrics, channelUnits, snorkelFish, snorkelFishBinned,
                                snorkelFishSteelheadBinned)
    # print json.dumps(channelUnitMetrics, indent=4, sort_keys=True)
    channelUnitJsonFilePath = "data/visit_{0}_channelUnitFishCounts.json".format(visit_id)
    with open(channelUnitJsonFilePath, 'w') as outfile:
        json.dump(channelUnitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    tier1Metrics = []
    infoLog("Calculate Fish Count Metrics for Tier1s for Visit {0}".format(visit_id))
    tier1FishCountMetrics(visit_id, tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned,
                          snorkelFishSteelheadBinned)
    # print json.dumps(tier1Metrics, indent=4, sort_keys=True)
    tier1JsonFilePath = "data/visit_{0}_tier1FishCounts.json".format(visit_id)
    with open(tier1JsonFilePath, 'w') as outfile:
        json.dump(tier1Metrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    infoLog("Writing Metrics for Visit {0} to Azure Blob storage".format(visit_id))
    block_blob_service.create_blob_from_path(container_name, "visit_{0}/visit_metrics.json".format(visit_id), visitJsonFilePath)
    block_blob_service.create_blob_from_path(container_name, "visit_{0}/channel_unit_metrics.json".format(visit_id), channelUnitJsonFilePath)
    block_blob_service.create_blob_from_path(container_name, "visit_{0}/tier1_metrics.json".format(visit_id), tier1JsonFilePath)


def infoLog(message):
    logging.info(message)
    print message


if __name__ == "__main__":
    main()