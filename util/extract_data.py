import os
import sys

import urllib3
import json
import joblib


class ExtractData:

    stack_exchange_tags = []
    stack_exchange_url = ""
    tags_file_url = ""
    http = None

    def __init__(self, stack_exchange_url, tags_file_url):
        self.stack_exchange_url = stack_exchange_url
        self.tags_file_url = tags_file_url + "datascience_stackexchange_tag.joblib"
        self.http = urllib3.PoolManager()

    def extractTagsFromData(self, data):
        json_data = json.loads(data)
        for item in json_data["items"]:
            self.stack_exchange_tags.append(item["tags"])

    def getDataFromApi(self):
        for i in range(1, 101):
            url = self.stack_exchange_url.partition("=")
            url = url[0] + url[1] + str(i) + url[2][1:]
            response = self.http.request('GET', url)
            if(response.status == 200):
                self.extractTagsFromData(response.data)
            else:
                continue
        self.writeExtractedTagsInPickelFile()

    def writeExtractedTagsInPickelFile(self):
        joblib.dump(self.stack_exchange_tags, self.tags_file_url)

    def loadTagsFromFile(self):
        if(os.path.isfile(self.tags_file_url)):
            self.stack_exchange_tags = joblib.load(self.tags_file_url)

    def extractData(self):
        if (not os.path.isfile(self.tags_file_url)):
            print("File not present... downloading data...", file=sys.stdout)
            self.getDataFromApi()
        elif (len(self.stack_exchange_tags) == 0):
            print("Reading from the file.......\n", file=sys.stdout)
            self.loadTagsFromFile()
        else:
            print("No need of reading from file....", file=sys.stdout)
