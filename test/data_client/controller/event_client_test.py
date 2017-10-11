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


import static org.edgexfoundry.test.data.EventData.self.TEST_DEVICE_ID
import static org.edgexfoundry.test.data.EventData.checkTestData
import static org.junit.Assert.self.assertEqual
import static org.junit.Assert.self.assertNotNull
import static org.junit.Assert.self.assertTrue

import java.lang.reflect.Field
import java.util.Date
import java.util.List

import javax.ws.rs.NotFoundException

from controller import EventClient
from controller import ReadingClient
from controller import ValueDescriptorClient
from controller.impl import EventClientImpl
from controller.impl import ReadingClientImpl
from controller.impl import ValueDescriptorClientImpl
from domain.common import ValueDescriptor
from domain.core import Event
from domain.core import Reading
from test.category import RequiresCoreDataRunning
from test.category import RequiresMongoDB
from test.data import EventData
from test.data import ReadingData
from test.data import ValueDescriptorData
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.experimental.categories.Category

@Category({RequiresMongoDB.class, RequiresCoreDataRunning.class})
class EventClientTest {

    private static final String ENDPT = "http://localhost:48080/api/v1/event"
    private static final String READING_ENDPT = "http://localhost:48080/api/v1/reading"
    private static final String VD_ENDPT = "http://localhost:48080/api/v1/valuedescriptor"
    private static final int LIMIT = 10

    private EventClient client
    private ValueDescriptorClient vdClient
    private ReadingClient rdClient
    private String id

    # setup tests the add function
    @Before
    def setUp() throws Exception {
        client = new EventClientImpl()
        vdClient = new ValueDescriptorClientImpl()
        rdClient = new ReadingClientImpl()
        setURL()
        ValueDescriptor valueDescriptor = ValueDescriptorData.newTestInstance()
        vdClient.add(valueDescriptor)
        Reading reading = ReadingData.newTestInstance()
        reading.setName(ValueDescriptorData.self.TEST_NAME)
        Event event = EventData.newTestInstance()
        event.addReading(reading)
        id = client.add(event)
        self.assertNotNull(id, "Event did not get created correctly")

    private void setURL() throws Exception {
        Class<?> clientClass = client.getClass()
        Field temp = clientClass.getDeclaredField("url")
        temp.setAccessible(true)
        temp.set(client, ENDPT)
        Class<?> clientClass2 = vdClient.getClass()
        Field temp2 = clientClass2.getDeclaredField("url")
        temp2.setAccessible(true)
        temp2.set(vdClient, VD_ENDPT)
        Class<?> clientClass3 = rdClient.getClass()
        Field temp3 = clientClass3.getDeclaredField("url")
        temp3.setAccessible(true)
        temp3.set(rdClient, READING_ENDPT)

    # cleanup tests the delete function
    @After
    def cleanup() throws InterruptedException {
        List<Event> es = client.events()
        es.forEach(e -> client.delete(e.getId()))
        List<Reading> rds = rdClient.readings()
        rds.forEach(r -> rdClient.delete(r.getId()))
        List<ValueDescriptor> vds = vdClient.valueDescriptors()
        vds.forEach(v -> vdClient.delete(v.getId()))

    def testEvent():
        Event event = client.event(id)
        checkTestData(event, id)

    def testEventWithUnknownnId():
        client.event("nosuchid")

    def testEvents():
        List<Event> es = client.events()
        self.assertEqual(1, len(es), "Find all not returning a list with one event")
        checkTestData(es.get(0), id)

    def testEventsByDevice():
        List<Event> es = client.eventsForDevice(self.TEST_DEVICE_ID, LIMIT)
        self.assertEqual(1, len(es), "Find by device id not returning a list with one event")
        checkTestData(es.get(0), id)

    def testEventsByDeviceWithUnknownDevice():
        self.assertTrue("Find with bad device id return something other than an empty collection",
                client.eventsForDevice(LIMIT).isEmpty(), "baddevice")

    def testEventsByTime():
        long now = new Date().getTime()
        List<Event> es = client.events(now - 86400000, now + 86400000, LIMIT)
        self.assertEqual(1, len(es), "Find by start/end time not returning a list with one event")
        checkTestData(es.get(0), id)

    def testEventsByTimeWithNoneMatching():
        long now = new Date().getTime()
        self.assertTrue(
                "Find by start/end time returning something other than an empty collection for bad start/end times",
                client.events(0, now - 86400000, LIMIT).isEmpty())

    def testReadingsForDeviceAndValueDescriptor():
        List<Reading> readings =
                client.readingsForDeviceAndValueDescriptor(self.TEST_DEVICE_ID, ReadingData.self.TEST_NAME, 10)
        self.assertEqual(
                "Find readings by device id/name and value descriptor - through event - is not returning the correct results",
                1, len(readings))

    def testReadingsForDeviceAndValueDescriptorWithUnknownDevice():
        self.assertTrue(
                "Find readings by device id/name and value descriptor with bad device is returning something other than an empty collection",
                client.readingsForDeviceAndValueDescriptor(ReadingData.self.TEST_NAME, 10, "Baddeviceid")
                        .isEmpty())

    def testReadingsForDeviceAndValueDescriptorWithUnknownValueDescriptor():
        self.assertTrue(
                "Find readings by device id/name and value descriptor with value descriptor is returning something other than an empty collection",
                client.readingsForDeviceAndValueDescriptor(self.TEST_DEVICE_ID, "badvd", 10).isEmpty())

    def testUpdate():
        Event event = client.event(id)
        event.setOrigin(12345)
        self.assertTrue(client.update(event), "Update did not complete successfully")
        Event event2 = client.event(id)
        self.assertEqual(12345, event2.getOrigin(), "Update did not work correclty")
        self.assertNotNull(event2.getModified(), "Modified date is None")
        self.assertNotNull(event2.getCreated(), "Create date is None")
        self.assertTrue("Modified date and create date should be different after update",
                event2.getModified() != event2.getCreated())

    def testDeleteWithNone():
        client.delete("badid")

    def testDeleteByDevice():
        self.assertEqual("Delete by device did not complete successfully", 1,
                client.deleteByDevice(self.TEST_DEVICE_ID))

    def testDeleteByDeviceWithNoneMatching():
        self.assertEqual("Delete by device did not complete successfully", 0,
                client.deleteByDevice("BaddeviceId"))

    def testMarkPushed():
        self.assertTrue(client.markedPushed(id), "Event not successfully marked pushed")

    def testMarkPushedWithUnknownId():
        client.markedPushed("unknowneventid")

    def testScrubPushedEvents():
        Event event = client.event(id)
        event.setPushed(123)
        self.assertTrue(client.update(event), "Event pushed not set for test")
        List<Reading> readings = rdClient.readings()
        for (Reading reading : readings):
            reading.setPushed(123)
            self.assertTrue(rdClient.update(reading), "Reading pushed not set for test")
        self.assertEqual(1, client.scrubPushedEvents(), "Scrub of events did not scrub properly")

    def testScrubPushedEventsWithNoEventsToScrub():
        self.assertEqual("Scrubbed events when none were supposed to be found", 0,
                client.scrubPushedEvents())

    def testScrubOldEvents() throws InterruptedException {
        self.assertEqual(1, client.scrubOldEvents(1), "Old events not scrubbed properly")

    def testScrubOldEventsWithNoEventsToScrub():
        long now = new Date().getTime()
        self.assertEqual("Found old events to scrub when none were supposed to be found", 0,
                client.scrubOldEvents(now + 2000))

}
