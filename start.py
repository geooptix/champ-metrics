
import argparse
import json
import ConfigParser

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
    parser.add_argument('visitID', help='Visit ID', type=int)
    args = parser.parse_args()

    if not args.visitID:
        print "ERROR: Missing arguments"
        parser.print_help()
        exit(1)

    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    clientID = ConfigSectionMap("credentials")["clientid"]
    clientSecret = ConfigSectionMap("credentials")["clientsecret"]
    username = ConfigSectionMap("credentials")["username"]
    password = ConfigSectionMap("credentials")["password"]

    tokenUrl = ConfigSectionMap("api")["tokenurl"]
    baseApiUrl = ConfigSectionMap("api")["baseapiurl"]

    logging.basicConfig(filename=args.logFile, level=logging.INFO)

    tokenizer = Tokenator.Tokenator(tokenUrl,clientID,clientSecret,username,password)

    apiHelper = ApiHelper.ApiHelper(baseApiUrl, tokenizer.TOKEN)

    visit_id = args.visitID
    visit = apiHelper.getVisit(visit_id)
    protocol = visit["protocol"]
    iteration = str(visit["iterationID"] + 2010)

    logging.info(str(visit_id) + " - " + protocol + ": " + iteration)
    print str(visit_id) + " - " + protocol + ": " + iteration

    snorkelFish = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish")
    snorkelFishBinned = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish Count Binned")
    snorkelFishSteelheadBinned = apiHelper.getVisitMeasurements(visit_id, "Snorkel Fish Count Steelhead Binned")

    #print "Writing Visit data to file"
    #visit_file = 'data/visit_{}.json'.format(visit_id)
    #with open(visit_file, 'w') as outfile:
    #    json.dump(visit, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    #print json.dumps(snorkelFish, indent=4, sort_keys=True)
    #print json.dumps(snorkelFishBinned, indent=4, sort_keys=True)
    #print json.dumps(snorkelFishSteelheadBinned, indent=4, sort_keys=True)

    visitMetrics = dict()
    logging.info("Calculate Fish Count Metrics for Visit")
    print "Calculate Fish Count Metrics for Visit"
    visitFishCountMetrics(visit_id, visitMetrics, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
    #print json.dumps(visitMetrics, indent=4, sort_keys=True)

    with open("data/fishCounts.json", 'w') as outfile:
        json.dump(visitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    channelUnits = apiHelper.getVisitMeasurements(visit_id, "Channel Unit")

    channelUnitMetrics = []
    logging.info("Calculate Fish Count Metrics for Channel Units")
    print "Calculate Fish Count Metrics for Channel Units"
    channelUnitFishCountMetrics(visit_id, channelUnitMetrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
    #print json.dumps(channelUnitMetrics, indent=4, sort_keys=True)

    with open("data/channelUnitFishCounts.json", 'w') as outfile:
        json.dump(channelUnitMetrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    tier1Metrics = []
    logging.info("Calculate Fish Count Metrics for Tier1s")
    print "Calculate Fish Count Metrics for Tier1s"
    tier1FishCountMetrics(visit_id, tier1Metrics, channelUnits, snorkelFish, snorkelFishBinned, snorkelFishSteelheadBinned)
    #print json.dumps(tier1Metrics, indent=4, sort_keys=True)

    with open("data/tier1FishCounts.json", 'w') as outfile:
        json.dump(tier1Metrics, outfile, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()