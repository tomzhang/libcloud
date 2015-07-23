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
Common settings and connection objects for Ucloud Cloud
"""
import hashlib, json
from libcloud.utils.py3 import httplib, urlparse
from libcloud.common.base import ConnectionUserAndKey, ConnectionKey
from libcloud.common.base import JsonResponse
from libcloud.common.types import InvalidCredsError
from config import UCLOUD_PRIVATE_KEY as private_key
import sys

__all__ = {
	'API_HOST',
	'API_ROOT',
	'Ucloud_Response',
	'Ucloud_Connection'
}


# Endpoint for the Ucloud API
API_HOST = 'api.ucloud.cn'
API_ROOT = '/'


def _verfy_ac(private_key, params):
    """
    private key verafication and encoding action
    """
    items = params.items()
    items.sort()

    params_data = ""
    for key, value in items:
        params_data = params_data + str(key) + str(value)

    params_data = params_data+private_key

    '''use sha1 to encode keys'''
    hash_new = hashlib.sha1()
    hash_new.update(params_data)
    hash_value = hash_new.hexdigest()
    return hash_value

class Ucloud_Response(JsonResponse):
	valid_response_codes = [httplib.OK, httplib.ACCEPTED, httplib.CREATED,
                            httplib.NO_CONTENT]
	def parse_error(self):
        	if self.status == httplib.UNAUTHORIZED:
            		body = self.parse_body()
            		raise InvalidCredsError(body['message'])
        	else:
            		body = self.parse_body()
            		if 'message' in body:
                		error = '%s (code: %s)' % (body['message'], self.status)
            		else:
                		error = body
            		return error




class UConnection(ConnectionUserAndKey):
	"""
	Connection class to connect to Ucloud's API servers
	"""
	host = API_HOST 
	responseCLs = Ucloud_Response
	

	def add_default_params(self, params):
        	"""
        	Add parameters that are necessary for every request
		This method adds ``client_id`` and ``api_key`` to
        	the request.
        	"""
		params['PublicKey'] = self.user_id
		self.private_key = private_key
		params['Signature'] = _verfy_ac(self.private_key, params)
        	return params
