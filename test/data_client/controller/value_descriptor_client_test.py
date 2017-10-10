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


import static org.edgexfoundry.test.data.ValueDescriptorData.self.TEST_LABELS
import static org.edgexfoundry.test.data.ValueDescriptorData.self.TEST_NAME
import static org.edgexfoundry.test.data.ValueDescriptorData.self.TEST_UOMLABEL
import static org.edgexfoundry.test.data.ValueDescriptorData.checkTestData
import static org.junit.Assert.self.assertEqual
import static org.junit.Assert.self.assertNotNull
import static org.junit.Assert.self.assertTrue

import java.lang.reflect.Field
import java.util.List

import javax.ws.rs.NotFoundException

from controller import ValueDescriptorClient
from controller.impl import ValueDescriptorClientImpl
from domain.common import ValueDescriptor
from test.category import RequiresCoreDataRunning
from test.category import RequiresMongoDB
from test.data import DeviceData
from test.data import ValueDescriptorData
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.experimental.categories.Category

@Category({RequiresMongoDB.class, RequiresCoreDataRunning.class})
class ValueDescriptorClientTest {

    private static final String ENDPT = "http://localhost:48080/api/v1/valuedescriptor"

    private ValueDescriptorClient client
    private String id

    # setup tests the add function
    @Before
    def setUp() throws Exception {
        client = new ValueDescriptorClientImpl()
        setURL()
        ValueDescriptor valueDescriptor = ValueDescriptorData.newTestInstance()
        id = client.add(valueDescriptor)
        self.assertNotNull(id, "Value Descriptor did not get created correctly")

    private void setURL() throws Exception {
        Class<?> clientClass = client.getClass()
        Field temp = clientClass.getDeclaredField("url")
        temp.setAccessible(true)
        temp.set(client, ENDPT)

    # cleanup tests the delete function
    @After
    def cleanup():
        List<ValueDescriptor> valueDescriptors = client.valueDescriptors()
        valueDescriptors.forEach((valueDescriptor) -> client.delete(valueDescriptor.getId()))

    def testValueDescriptor():
        ValueDescriptor vd = client.valueDescriptor(id)
        checkTestData(vd, id)

    def testValueDescriptorWithUnknownnId():
        client.valueDescriptor("nosuchid")

    def testValueDescriptors():
        List<ValueDescriptor> vds = client.valueDescriptors()
        self.assertEqual(1, len(vds), "Find all not returning a list with one value descriptor")
        checkTestData(vds.get(0), id)

    def testValueDescriptorForName():
        ValueDescriptor vd = client.valueDescriptorByName(self.TEST_NAME)
        checkTestData(vd, id)

    def testValueDescriptorForNameWithNoneMatching():
        client.valueDescriptorByName("badname")

    def testValueDescriptorsByLabel():
        List<ValueDescriptor> vds = client.valueDescriptorByLabel(self.TEST_LABELS[0])
        self.assertEqual(1, len(vds), "Find by label not returning a list with one value descriptor")
        checkTestData(vds.get(0), id)

    def testValueDescriptorsForDeviceByName():
        client.valueDescriptorsForDeviceByName(DeviceData.self.TEST_NAME)

    def testValueDescriptorsForDeviceById():
        client.valueDescriptorsForDeviceById("123")

    def testValueDescriptorsByLabelWithNoneMatching():
        List<ValueDescriptor> vds = client.valueDescriptorByLabel("badlabel")
        self.assertTrue(vds.isEmpty(), "ValueDescriptor found with bad label")

    def testValueDescriptorsByUoMLabel():
        List<ValueDescriptor> vds = client.valueDescriptorByUOMLabel(self.TEST_UOMLABEL)
        self.assertEqual(1, len(vds), "Find by UOM label not returning a list with one value descriptor")
        checkTestData(vds.get(0), id)

    def testValueDescriptorsByUOMLabelWithNoneMatching():
        List<ValueDescriptor> vds = client.valueDescriptorByUOMLabel("badlabel")
        self.assertTrue(vds.isEmpty(), "ValueDescriptor found with bad UOM label")

    # TODO - in the future have Metadata up and also test with devices
    # associated
    def valueDescriptorsForDeviceByName():
        client.valueDescriptorsForDeviceByName("unknowndevice")

    # TODO - in the future have Metadata up and also test with devices
    # associated
    def valueDescriptorsForDeviceById():
        client.valueDescriptorsForDeviceById("unknowndeviceid")

    def testDeleteWithNone():
        client.delete("badid")

    def testUpdate():
        ValueDescriptor vd = client.valueDescriptor(id)
        vd.setOrigin(12345)
        self.assertTrue(client.update(vd), "Update did not complete successfully")
        ValueDescriptor vd2 = client.valueDescriptor(id)
        self.assertEqual(12345, vd2.getOrigin(), "Update did not work correclty")
        self.assertNotNull(vd2.getModified(), "Modified date is None")
        self.assertNotNull(vd2.getCreated(), "Create date is None")
        self.assertTrue("Modified date and create date should be different after update",
                vd2.getModified() != vd2.getCreated())

    def testDeleteByName():
        self.assertTrue(client.deleteByName(self.TEST_NAME), "ValueDescriptor not deleted by name")

    def testDeleteByNameWithNone():
        client.deleteByName("badname")

}
