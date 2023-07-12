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


"""Command to create a moggy."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base


import cazt.util_run_helper


DETAILED_HELP = {
    'EXAMPLES':
        """\
            TODO write the customer facing documentation
        """
}


class Create(base.Command):
  r"""Create a moggy.
  """

  detailed_help = DETAILED_HELP

  @staticmethod
  def Args(parser):
    parser.add_argument(
      '--name',
      help='The name of your pet.',
      required=True
      )

    parser.add_argument(
      '--activity-log-object-storage',
      help='The storage location. Just the name not a URI.',
      required=True
      )

    parser.add_argument(
      '--description',
      help='The description. Business requirements require allowing any printable character.',
      required=False
      )

    parser.add_argument(
      '--api-endpoint-overrides',
      help='The BASE URL to use for the API endpoint: Example: https://cazt.gcloud.localtest.me:8443/uat',
      required=False
      )


  def Run(self, args):
    request_content_body_payload = {
      "Name": args.name,
      "ActivityLogObjectStorage": args.activity_log_object_storage
	}
    if args.description:
      request_content_body_payload["Description"] = args.description

    API_ENDPOINT_PATH = "createmoggy"  # no leading /

    return cazt.util_run_helper.RunHelper(
      args.api_endpoint_overrides,
      API_ENDPOINT_PATH,
      request_content_body_payload,
      args.account
      )
