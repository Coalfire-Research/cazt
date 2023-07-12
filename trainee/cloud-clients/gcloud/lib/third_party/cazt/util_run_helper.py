# Copyright © 2023 Coalfire

# Original code modified from Google's (https://cloud.google.com/sdk/docs/resources)
#   Google Cloud SDK 426.0.0
# Original code license was
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#     
#        http://www.apache.org/licenses/LICENSE-2.0
#     
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.


from googlecloudsdk.core import requests
from googlecloudsdk.core import transport
from googlecloudsdk.core import requests
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import log

import base64
import json



def RunHelper(api_endpoint_overrides, api_endpoint_path, request_content_body_payload, account):
  if not api_endpoint_overrides:
    raise exceptions.InvalidArgumentException(
        'api-endpoint-overrides',
        'The default API endpoint would have been production. Try setting a non-production endpoint.')

  if account:
      authn = str(base64.b64encode(account.encode("utf-8")), "utf-8")
  else:
      # We don't support the default account (avoids leaking real credentials)
      authn = str(base64.b64encode("default account not supported".encode("utf-8")), "utf-8")

  # We didn't use urljoin as it is messy with values such as
  #     https://localhost/uat   +  someApiWithNoLeadingSlash    ==> https://localhost/someApiWithNoLeadingSlash
  #     instead of the desired https://localhost/uat/someApiWithNoLeadingSlash
  endpoint_url = api_endpoint_overrides
  if not endpoint_url.endswith("/"):
    endpoint_url += "/"
  endpoint_url += api_endpoint_path

  # Auto-provides the user-agent header already
  http_client = requests.GetSession()

  response = http_client.post(endpoint_url, 
      json = request_content_body_payload,
      headers = {"Authorization": f"Bearer {authn}"}
      )

  if response:
    log.debug(response.status_code)
    log.debug(response.headers)
    log.debug(response.text)

  if 200 != response.status_code:
    error_message = f"{response.status_code}    {response.text}"
    log.error(error_message)
    return error_message
  elif "<html><head><title>Burp Suite Professional</title>" in response.text:
    # Burp Suite has an annoying behavior where it returns an HTTP 200 even if the connection failed
    log.error("HTTP Proxy returned an error message. Is the simulator running and your api-endpoint-overrides correct?")
    return response.text
  else:
    parsed_json = json.loads(response.text)

    return parsed_json
