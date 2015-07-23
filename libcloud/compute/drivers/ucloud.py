# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Ucloud Driver
"""
import hashlib, json, httplib
from libcloud.utils.py3 import httplib, urlparse
from libcloud.common.ucloud import API_ROOT, UConnection
from libcloud.compute.types import Provider, NodeState
from libcloud.compute.base import NodeDriver, NodeSize, Node, NodeLocation
from libcloud.compute.base import NodeAuthPassword, NodeAuthSSHKey
from libcloud.compute.base import NodeImage, StorageVolume

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class UcloudNodeDriver(NodeDriver):
    """libcloud driver for the Linode API

    Rough mapping of which is which:

        list_nodes              ucloud.list
        reboot_node             ucloud.reboot
        destroy_node            ucloud.delete
        create_node             ucloud.create, ucloud.update,
                                ucloud.disk.createfromdistribution,
                                ucloud.disk.create, ucloud.config.create,
                                ucloud.ip.addprivate, ucloud.boot
        list_sizes              avail.ucloudplans
        list_images             avail.distributions
        list_locations          avail.datacenters
        list_volumes            ucloud.disk.list
        destroy_volume          ucloud.disk.delete

    For more information on the Linode API, be sure to read the reference:

        http://http://docs.ucloud.cn/api/overview.html
    """
    type = Provider.UCLOUD
    name = "Ucloud"
    website = 'https://api.ucloud.cn'
    features = {'create_node': ['ssh_key', 'password']}
    connectionCls = UConnection
    NODE_STATE_MAP = {
       'running': NodeState.RUNNING,
       'stopped': NodeState.STOPPED,
    }
    
    def list_nodes(self):	
    	params = {"Action": "DescribeUHostInstance",
		"Region":"cn-north-03",
		"Limit":"100",
		}
   	data = self.connection.request(API_ROOT, params=params).object
	#results = json.loads(data)
	#return json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))
	return data
