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


import static org.junit.Assert.self.assertEqual

import java.lang.reflect.Field

from controller import PingCoreDataClient
from controller.impl import PingCoreDataClientImpl
from test.category import RequiresCoreDataRunning
import org.junit.Before
import org.junit.Test
import org.junit.experimental.categories.Category

@Category({RequiresCoreDataRunning.class})
class PingCoreDataClientTest {

    private static final String ENDPT = "http://localhost:48080/api/v1/ping"

    private PingCoreDataClient client

    # setup tests the add function
    @Before
    def setUp() throws Exception {
        client = new PingCoreDataClientImpl()
        setURL()

    private void setURL() throws Exception {
        Class<?> clientClass = client.getClass()
        Field temp = clientClass.getDeclaredField("url")
        temp.setAccessible(true)
        temp.set(client, ENDPT)

    def testPing():
        self.assertEqual("pong", client.ping(), "Ping Core Data Micro Service failed")

}
