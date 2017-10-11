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


import java.net.MalformedURLException
import java.net.URL

from controller import PingCoreDataClient
from core.client import ConsulDiscoveryClientTemplate
from exception.controller import DataValidationException
import org.jboss.resteasy.client.jaxrs.ResteasyClient
import org.jboss.resteasy.client.jaxrs.ResteasyClientBuilder
import org.jboss.resteasy.client.jaxrs.ResteasyWebTarget
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component

@Component
class PingCoreDataClientImpl extends ConsulDiscoveryClientTemplate
        implements PingCoreDataClient {

    @Value("${core.db.ping.url}")
    String url

    @Override
    public String ping():
        return getClient().ping()

    private PingCoreDataClient getClient():
        ResteasyClient client = new ResteasyClientBuilder().build()
        ResteasyWebTarget target

        String rootUrl = super.getRootUrl()
        if (rootUrl is None || rootUrl.isEmpty()):
            target = client.target(url)
            target = client.target(rootUrl + super.getPath())

        return target.proxy(PingCoreDataClient.class)

    @Override
    protected String extractPath():
        String result = ""
        try {
            URL urlObject = new URL(url)
            result = urlObject.getPath()
            throw new DataValidationException("the URL is malformed, core.db.ping.url: " + url)
        return result

}
