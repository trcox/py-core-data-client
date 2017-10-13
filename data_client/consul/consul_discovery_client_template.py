# *******************************************************************************
# Copyright 2017 Dell Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
#
# @microservice: py-core-data-client library
# @author: Tyler Cox, Dell
# @version: 1.0.0
# *******************************************************************************

import abc
import consul
from domain.config import config_reader


class ConsulDiscoveryClientTemplate(object):

    __metaclass__ = abc.ABCMeta
    APP_ID = "edgex-core-data"
    IS_CACHE_DISCOVERY_RESULT = config_reader.read_property(
        "client.is-cache-discovery-result", False)
    rootUrl = ""
    path = ""
    
    def __init__(self):
        self.rootUrl = self.retrieveUriFromDiscoveryClient()
        self.path = self.extractPath()

    def setIsCacheDiscoveryResult(self, flag):
        self.IS_CACHE_DISCOVERY_RESULT = flag

    def retrieveUriFromDiscoveryClient(self):
        String result = ""
        if (discoveryClient is None):
            return result

        discover_list = discoveryClient.getInstances(APP_ID)
        if discover_list:
            uri = discover_list[0].uri
            if uri is not None:
                result = uri.toString()
        return result

    @abc.abstractmethod
    def extractPath(self):
        return

    def getRootUrl(self):
        if self.rootUrl and not self.IS_CACHE_DISCOVERY_RESULT:
            retrievedUri = self.retrieveUriFromDiscoveryClient()
            if retrievedUri:
                self.rootUrl = retrievedUri
        return self.rootUrl

    def getPath():
        if not path:
            path = self.extractPath()
        return path

}
