import json

import requests


class ApiHelper:
    """

    """

    base_url = ""
    token = None

    def __init__(self, url, token):
        self.base_url = url
        self.token = token


    def getVisits(self):
        """
        Get all the instances we need to delete
        :param schemaName:
        :return:
        """

        print "Getting visit data"
        url = "{0}/visits".format(self.base_url)
        response = requests.get(url, headers={"Authorization": self.token})
        respObj = json.loads(response.content)

        visits = {}
        for obj in respObj:
            visits[obj['id']] = obj

        return visits

    def rawCall(self, url, absolute=False):
        print "Making Call: {}".format(url)
        if absolute == False:
            url = "{0}/{1}".format(self.base_url, url)

        retry = True
        retries = 0
        # Really basic retry functionality.
        # TODO: This catches "connection reset by peer" but not error status codes like 404 or 500
        while retry and retries < 10:
            try:
                retries += 1
                response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
                retry = False
            except Exception, e:
                print "ERROR: Problem with API Call: {}. retrying... {}".format(url, retries)
        respObj = json.loads(response.content)

        return respObj

    def getMetricSchema(self):
        print "Getting Metric Schemas"
        url = "{0}/metricschemas".format(self.base_url)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        respObj = json.loads(response.content)

        return respObj

    def getSites(self):
        print "Getting sites"
        url = "{0}/sites".format(self.base_url)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        respObj = json.loads(response.content)

        return respObj

    def getWatersheds(self):
        print "Getting watersheds"
        url = "{0}/watersheds".format(self.base_url)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        respObj = json.loads(response.content)

        watersheds = {}
        for obj in respObj:
            response = requests.get(obj['url'], headers={"Authorization": self.token}, verify=self.shouldVerify())
            respObj = json.loads(response.content)
            watersheds[obj['name']] = [site['name'] for site in respObj['sites']]
            print "     Getting sites for watershed: {}".format(obj['name'])

        return watersheds

    def downloadFile(self, url, localpath):
        print "Getting visit file data"
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        with open(localpath, 'wb') as f:
            f.write(response.content)
            print "Downloaded file: {} to: {}".format(url, localpath)

    def getVisit(self, visitID):
        """
        Get all the instances we need to delete
        :param schemaName:
        :return:
        """
        print "Getting visit data"
        url = "{0}/visits/{1}".format(self.base_url, visitID)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())

        if response.status_code != 200:
            return None

        respObj = json.loads(response.content)

        return respObj


    def getVisitFieldFiles(self, visitID):
        """
        Get all the instances we need to delete
        :param schemaName:
        :return:
        """
        print "Getting visit file data"
        url = "{0}/visits/{1}/fieldFolders".format(self.base_url, visitID)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        respObj = json.loads(response.content)

        files = {}
        counter = 0
        for folder in respObj:
            url = "{0}/visits/{1}/fieldFolders/{2}".format(self.base_url, visitID, folder['name'])
            response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
            respObj = json.loads(response.content)
            files[folder['name']] = respObj
            counter += len(respObj)

        print "  -- Found {} field files for the visit {}".format(counter, visitID)
        return files

    def getVisitMeasurements(self, visitID, measurementName):
        """
        Get all the instances
        :param measurementName:
        :return:
        """
        print "Getting visit measurements for visit " + str(visitID) + " of type " + measurementName
        url = "{0}/visits/{1}/measurements/{2}".format(self.base_url, visitID, measurementName)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())

        if response.status_code != 200:
            return None

        respObj = json.loads(response.content)

        return respObj

    def getInstances(self, schemaName):
        """
        Get all the instances we need to delete
        :param schemaName:
        :return:
        """
        print "Getting instances"
        url = "{0}/visit/metricschemas/{1}".format(self.base_url, schemaName)
        response = requests.get(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
        respObj = json.loads(response.content)
        print "  -- Found {} instances for the schema {}".format(len(respObj['instances']), schemaName)
        return [inst['url'] for inst in respObj['instances']]

    def deleteInstances(self, instances):
        """

        :param instances:
        :return:
        """
        counter = 0
        print "Deleting all {} existing instances:".format(len(instances))

        custom_options = {
            'start': 0,
            'end': 100,
            'width': 60,
            'blank': '_',
            'fill': '#',
            'format': '%(progress)s%% [%(fill)s%(blank)s]'
        }
        # progbar = ProgressBar(**custom_options)

        try:
            for url in instances:
                response = requests.delete(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
                respObj = json.loads(response.content)
                if response.status_code != 200:
                    raise "FAILED with code: {} and error: '{}'".format(response.status_code, response.text)
                counter += 1
                # progbar.progress = math.floor(float(counter) / float(len(instances)) * 100)
                # sys.stdout.write("\r {} {} of {}".format(str(progbar), counter, len(instances)))

        except Exception, e:
            print " FAILED after deleting {} instances".format(counter)
            raise "FAIL"

        print "  -- deleted {} instances".format(len(instances))
        return [inst['url'] for inst in respObj['instances']]

    def deleteSchema(self, schemaName):
        try:
            instances = self.getInstances(schemaName)

            # if not query_yes_no("\nIt's still not too late. Are you sure?"):
            #    return

            success = self.deleteInstances(instances)

            url = "{0}/visit/metricschemas/{1}".format(self.base_url, schemaName)
            response = requests.delete(url, headers={"Authorization": self.token}, verify=self.shouldVerify())
            respObj = json.loads(response.content)
            print "Schema Deleted"
            return [inst['url'] for inst in respObj['instances']]

        except Exception, e:
            print "whoops"

        print "boop"
        
    
    def shouldVerify(self):
        return False #'localhost' not in self.base_url
