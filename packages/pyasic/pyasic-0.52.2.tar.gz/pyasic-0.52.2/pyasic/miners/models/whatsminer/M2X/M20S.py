# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

from pyasic.miners.makes import WhatsMinerMake


class M20SV10(WhatsMinerMake):
    raw_model = "M20S V10"
    expected_chips = 105
    expected_fans = 2


class M20SV20(WhatsMinerMake):
    raw_model = "M20S V20"
    expected_chips = 111
    expected_fans = 2


class M20SV30(WhatsMinerMake):
    raw_model = "M20S V30"
    expected_chips = 140
    expected_fans = 2
