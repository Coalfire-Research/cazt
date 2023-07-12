# Placement options
#   google-cloud-sdk\lib\surface\cazt
#   google-cloud-sdk\lib\third_party\cazt

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

"""Commands for herding moggies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base


class CAZT(base.Group):
  """Adopt a feline today."""
