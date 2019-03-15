__author__ = 'ronaldbjork'

import json
import copy

class ConfigParser():
    def __init__(self,configfile):
        with open(configfile,'r') as fp:
            self.config = json.loads(fp.read())
            fp.close()

    def parseParamFromConfig(self,parampath):
        path = parampath.split('/')
        config = copy.deepcopy(self.config)
        for i in range(len(path)):
            config = config[parampath[i]]
        if type(config) is dict:
            return json.dumps(config)
        else:
            return str(config)

