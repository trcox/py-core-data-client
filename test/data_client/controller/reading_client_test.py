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


import static org.edgexfoundry.test.data.ReadingData.checkTestData
import static org.edgexfoundry.test.data.ValueDescriptorData.self.TEST_NAME
import static org.junit.Assert.self.assertEqual
import static org.junit.Assert.self.assertNotNull
import static org.junit.Assert.self.assertTrue

import java.lang.reflect.Field
import java.util.List

import javax.ws.rs.NotFoundException

from controller import ReadingClient
from controller import ValueDescriptorClient
from controller.impl import ReadingClientImpl
from controller.impl import ValueDescriptorClientImpl
from domain.common import IoTType
from domain.common import ValueDescriptor
from domain.core import Reading
from test.category import RequiresCoreDataRunning
from test.category import RequiresMongoDB
from test.data import DeviceData
from test.data import EventData
from test.data import ReadingData
from test.data import ValueDescriptorData
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.experimental.categories.Category

@Category({RequiresMongoDB.class, RequiresCoreDataRunning.class})
class ReadingClientTest {

    private static final String ENDPT = "http://localhost:48080/api/v1/reading"
    private static final String VD_ENDPT = "http://localhost:48080/api/v1/valuedescriptor"
    private static final int LIMIT = 10

    private ReadingClient client
    private ValueDescriptorClient vdClient
    private String id

    # setup tests the add function
    @Before
    def setUp() throws Exception {
        vdClient = new ValueDescriptorClientImpl()
        client = new ReadingClientImpl()
        setURL()
        ValueDescriptor valueDescriptor = ValueDescriptorData.newTestInstance()
        vdClient.add(valueDescriptor)
        Reading reading = ReadingData.newTestInstance()
        reading.setName(ValueDescriptorData.self.TEST_NAME)
        id = client.add(reading)
        self.assertNotNull(id, "Reading did not get created correctly")

    private void setURL() throws Exception {
        Class<?> clientClass = client.getClass()
        Field temp = clientClass.getDeclaredField("url")
        temp.setAccessible(true)
        temp.set(client, ENDPT)
        Class<?> clientClass2 = vdClient.getClass()
        Field temp2 = clientClass2.getDeclaredField("url")
        temp2.setAccessible(true)
        temp2.set(vdClient, VD_ENDPT)

    # cleanup tests the delete function
    @After
    def cleanup():
        List<Reading> readings = client.readings()
        readings.forEach((reading) -> client.delete(reading.getId()))
        List<ValueDescriptor> valueDescriptors = vdClient.valueDescriptors()
        valueDescriptors.forEach((valueDescriptor) -> vdClient.delete(valueDescriptor.getId()))

    def testReading():
        Reading reading = client.reading(id)
        checkTestData(reading, id)

    def testReadingWithUnknownnId():
        client.reading("nosuchid")

    def testReadings():
        List<Reading> readings = client.readings()
        self.assertEqual(1, len(readings), "Find all not returning a list with one reading")
        checkTestData(readings.get(0), id)

    def testReadingsForDevice(): # metadata not up and no devices in database
        List<Reading> readings = client.readings(DeviceData.self.TEST_NAME, LIMIT)
        self.assertEqual(0, len(readings), "Find all for device not returning a list with no reading")

    def testReadingByName():
        List<Reading> readings = client.readingsByName(self.TEST_NAME, LIMIT)
        checkTestData(readings.get(0), id)

    def testReadingForNameWithNoneMatching():
        self.assertTrue(client.readingsByName("badname", LIMIT).isEmpty(), "Reading found for bad name")

    def testReadingByNameAndDevice():
        List<Reading> readings = client.readingsByNameAndDevice(self.TEST_NAME, EventData.self.TEST_DEVICE_ID, LIMIT)
        checkTestData(readings.get(0), id)

    def testReadingForNameAndDeviceWithNoneMatching():
        self.assertTrue("Reading found for bad name and device",
                client.readingsByNameAndDevice("baddevice", LIMIT).isEmpty(), "badname")

    def testReadingsByLabel():
        List<Reading> readings = client.readingsByLabel(ValueDescriptorData.self.TEST_LABELS[0], LIMIT)
        self.assertEqual(1, len(readings), "Find by label not returning a list with one reading")
        checkTestData(readings.get(0), id)

    def testReadingsByLabelWithNoneMatching():
        List<Reading> readings = client.readingsByLabel(LIMIT, "badlabel")
        self.assertTrue(readings.isEmpty(), "Reading found with bad label")

    def testReadingsByUoMLabel():
        List<Reading> readings = client.readingsByUoMLabel(ValueDescriptorData.self.TEST_UOMLABEL, LIMIT)
        self.assertEqual(1, len(readings), "Find by UOM label not returning a list with one reading")
        checkTestData(readings.get(0), id)

    def testReadingsByUOMLabelWithNoneMatching():
        List<Reading> readings = client.readingsByUoMLabel(LIMIT, "badlable")
        self.assertTrue(readings.isEmpty(), "Reading found with bad UOM label")

    def testReadingsByType():
        List<Reading> readings = client.readingsByType(ValueDescriptorData.self.TEST_TYPE.toString(), LIMIT)
        self.assertEqual(1, len(readings), "Find by UOM label not returning a list with one reading")
        checkTestData(readings.get(0), id)

    def testReadingsByTypeWithNoneMatching():
        List<Reading> readings = client.readingsByType(IoTType.F.toString(), LIMIT)
        self.assertTrue(readings.isEmpty(), "Reading found with bad type")

    def testDeleteWithNone():
        client.delete("badid")

    def testUpdate():
        Reading reading = client.reading(id)
        reading.setOrigin(12345)
        self.assertTrue(client.update(reading), "Update did not complete successfully")
        Reading reading2 = client.reading(id)
        self.assertEqual(12345, reading2.getOrigin(), "Update did not work correclty")
        self.assertNotNull(reading2.getModified(), "Modified date is None")
        self.assertNotNull(reading2.getCreated(), "Create date is None")
        self.assertTrue("Modified date and create date should be different after update",
                reading2.getModified() != reading2.getCreated())

}
