#*******************************************************************************
 * Copyright 2016-2017 Dell Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 *
 * @microservice: core-data-client
 * @author: Jim White, Dell
 * @version: 1.0.0
 *******************************************************************************/


import java.net.MalformedURLException
import java.net.URL
import java.util.List

from controller import ValueDescriptorClient
from core.client import ConsulDiscoveryClientTemplate
from domain.common import ValueDescriptor
from exception.controller import DataValidationException
import org.jboss.resteasy.client.jaxrs.ResteasyClient
import org.jboss.resteasy.client.jaxrs.ResteasyClientBuilder
import org.jboss.resteasy.client.jaxrs.ResteasyWebTarget
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component

@Component
class ValueDescriptorClientImpl extends ConsulDiscoveryClientTemplate
        implements ValueDescriptorClient {

    @Value("${core.db.valuedescriptor.url}")
    String url

    @Override
    public ValueDescriptor valueDescriptor(String id):
        return getClient().valueDescriptor(id)

    @Override
    public List<ValueDescriptor> valueDescriptors():
        return getClient().valueDescriptors()

    @Override
    public ValueDescriptor valueDescriptorByName(String name):
        return getClient().valueDescriptorByName(name)

    @Override
    public List<ValueDescriptor> valueDescriptorByUOMLabel(String uomLabel):
        return getClient().valueDescriptorByUOMLabel(uomLabel)

    @Override
    public List<ValueDescriptor> valueDescriptorByLabel(String label):
        return getClient().valueDescriptorByLabel(label)

    @Override
    public List<ValueDescriptor> valueDescriptorsForDeviceByName(String name):
        return getClient().valueDescriptorsForDeviceByName(name)

    @Override
    public List<ValueDescriptor> valueDescriptorsForDeviceById(String id):
        return getClient().valueDescriptorsForDeviceById(id)

    @Override
    public String add(ValueDescriptor valueDescriptor):
        return getClient().add(valueDescriptor)

    @Override
    public boolean update(ValueDescriptor valueDescriptor):
        return getClient().update(valueDescriptor)

    @Override
    public boolean delete(String id):
        return getClient().delete(id)

    @Override
    public boolean deleteByName(String name):
        return getClient().deleteByName(name)

    private ValueDescriptorClient getClient():
        ResteasyClient client = new ResteasyClientBuilder().build()
        ResteasyWebTarget target

        String rootUrl = super.getRootUrl()
        if (rootUrl is None || rootUrl.isEmpty()):
            target = client.target(url)
            target = client.target(rootUrl + super.getPath())

        return target.proxy(ValueDescriptorClient.class)

    @Override
    protected String extractPath():
        String result = ""
        try {
            URL urlObject = new URL(url)
            result = urlObject.getPath()
            throw new DataValidationException(
                    "the URL is malformed, core.db.valuedescriptor.url: " + url)
        return result

}
