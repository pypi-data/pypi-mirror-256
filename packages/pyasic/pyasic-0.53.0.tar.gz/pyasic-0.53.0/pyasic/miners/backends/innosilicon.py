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
from typing import List, Optional

from pyasic.config import MinerConfig
from pyasic.data import Fan, HashBoard
from pyasic.data.error_codes import MinerErrorData
from pyasic.data.error_codes.innosilicon import InnosiliconError
from pyasic.errors import APIError
from pyasic.miners.backends import CGMiner
from pyasic.miners.data import (
    DataFunction,
    DataLocations,
    DataOptions,
    RPCAPICommand,
    WebAPICommand,
)
from pyasic.web.innosilicon import InnosiliconWebAPI

INNOSILICON_DATA_LOC = DataLocations(
    **{
        str(DataOptions.MAC): DataFunction(
            "_get_mac",
            [
                WebAPICommand("web_get_all", "getAll"),
                WebAPICommand("web_overview", "overview"),
            ],
        ),
        str(DataOptions.API_VERSION): DataFunction(
            "_get_api_ver",
            [RPCAPICommand("rpc_version", "version")],
        ),
        str(DataOptions.FW_VERSION): DataFunction(
            "_get_fw_ver",
            [RPCAPICommand("rpc_version", "version")],
        ),
        str(DataOptions.HASHRATE): DataFunction(
            "_get_hashrate",
            [
                RPCAPICommand("rpc_summary", "summary"),
                WebAPICommand("web_get_all", "getAll"),
            ],
        ),
        str(DataOptions.HASHBOARDS): DataFunction(
            "_get_hashboards",
            [
                RPCAPICommand("rpc_stats", "stats"),
                WebAPICommand("web_get_all", "getAll"),
            ],
        ),
        str(DataOptions.WATTAGE): DataFunction(
            "_get_wattage",
            [
                WebAPICommand("web_get_all", "getAll"),
                RPCAPICommand("rpc_stats", "stats"),
            ],
        ),
        str(DataOptions.WATTAGE_LIMIT): DataFunction(
            "_get_wattage_limit",
            [
                WebAPICommand("web_get_all", "getAll"),
            ],
        ),
        str(DataOptions.FANS): DataFunction(
            "_get_fans",
            [
                WebAPICommand("web_get_all", "getAll"),
            ],
        ),
        str(DataOptions.ERRORS): DataFunction(
            "_get_errors",
            [
                WebAPICommand("web_get_error_detail", "getErrorDetail"),
            ],
        ),
        str(DataOptions.UPTIME): DataFunction(
            "_get_uptime",
            [RPCAPICommand("rpc_stats", "stats")],
        ),
    }
)


class Innosilicon(CGMiner):
    """Base handler for Innosilicon miners"""

    _web_cls = InnosiliconWebAPI
    web: InnosiliconWebAPI

    data_locations = INNOSILICON_DATA_LOC

    supports_shutdown = True

    async def get_config(self) -> MinerConfig:
        # get pool data
        try:
            pools = await self.web.pools()
        except APIError:
            return self.config

        self.config = MinerConfig.from_inno(pools)
        return self.config

    async def reboot(self) -> bool:
        try:
            data = await self.web.reboot()
        except APIError:
            pass
        else:
            return data["success"]

    async def restart_cgminer(self) -> bool:
        try:
            data = await self.web.restart_cgminer()
        except APIError:
            pass
        else:
            return data["success"]

    async def restart_backend(self) -> bool:
        return await self.restart_cgminer()

    async def send_config(self, config: MinerConfig, user_suffix: str = None) -> None:
        self.config = config
        await self.web.update_pools(config.as_inno(user_suffix=user_suffix))

    ##################################################
    ### DATA GATHERING FUNCTIONS (get_{some_data}) ###
    ##################################################

    async def _get_mac(
        self, web_get_all: dict = None, web_overview: dict = None
    ) -> Optional[str]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        if web_get_all is None and web_overview is None:
            try:
                web_overview = await self.web.overview()
            except APIError:
                pass

        if web_get_all is not None:
            try:
                mac = web_get_all["mac"]
                return mac.upper()
            except KeyError:
                pass

        if web_overview is not None:
            try:
                mac = web_overview["version"]["ethaddr"]
                return mac.upper()
            except KeyError:
                pass

    async def _get_hashrate(
        self, rpc_summary: dict = None, web_get_all: dict = None
    ) -> Optional[float]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        if rpc_summary is None and web_get_all is None:
            try:
                rpc_summary = await self.rpc.summary()
            except APIError:
                pass

        if web_get_all is not None:
            try:
                if "Hash Rate H" in web_get_all["total_hash"].keys():
                    return round(
                        float(web_get_all["total_hash"]["Hash Rate H"] / 1000000000000),
                        2,
                    )
                elif "Hash Rate" in web_get_all["total_hash"].keys():
                    return round(
                        float(web_get_all["total_hash"]["Hash Rate"] / 1000000), 5
                    )
            except KeyError:
                pass

        if rpc_summary is not None:
            try:
                return round(float(rpc_summary["SUMMARY"][0]["MHS 1m"] / 1000000), 2)
            except (KeyError, IndexError):
                pass

    async def _get_hashboards(
        self, rpc_stats: dict = None, web_get_all: dict = None
    ) -> List[HashBoard]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        hashboards = [
            HashBoard(slot=i, expected_chips=self.expected_chips)
            for i in range(self.expected_hashboards)
        ]

        if rpc_stats is None:
            try:
                rpc_stats = await self.rpc.stats()
            except APIError:
                pass

        if web_get_all is None:
            try:
                web_get_all = await self.web.get_all()
            except APIError:
                pass
            else:
                web_get_all = web_get_all["all"]

        if rpc_stats is not None:
            if rpc_stats.get("STATS"):
                for board in rpc_stats["STATS"]:
                    try:
                        idx = board["Chain ID"]
                        chips = board["Num active chips"]
                    except KeyError:
                        pass
                    else:
                        hashboards[idx].chips = chips
                        hashboards[idx].missing = False

        if web_get_all is not None:
            if web_get_all.get("chain"):
                for board in web_get_all["chain"]:
                    idx = board.get("ASC")
                    if idx is not None:
                        temp = board.get("Temp min")
                        if temp:
                            hashboards[idx].temp = round(temp)

                        hashrate = board.get("Hash Rate H")
                        if hashrate:
                            hashboards[idx].hashrate = round(
                                hashrate / 1000000000000, 2
                            )

                        chip_temp = board.get("Temp max")
                        if chip_temp:
                            hashboards[idx].chip_temp = round(chip_temp)

        return hashboards

    async def _get_wattage(
        self, web_get_all: dict = None, rpc_stats: dict = None
    ) -> Optional[int]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        if web_get_all is None:
            try:
                web_get_all = await self.web.get_all()
            except APIError:
                pass
            else:
                web_get_all = web_get_all["all"]

        if web_get_all is not None:
            try:
                return web_get_all["power"]
            except KeyError:
                pass

        if rpc_stats is None:
            try:
                rpc_stats = await self.rpc.stats()
            except APIError:
                pass

        if rpc_stats is not None:
            if rpc_stats.get("STATS"):
                for board in rpc_stats["STATS"]:
                    try:
                        wattage = board["power"]
                    except KeyError:
                        pass
                    else:
                        wattage = int(wattage)
                        return wattage

    async def _get_fans(self, web_get_all: dict = None) -> List[Fan]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        if web_get_all is None:
            try:
                web_get_all = await self.web.get_all()
            except APIError:
                pass
            else:
                web_get_all = web_get_all["all"]

        fans = [Fan() for _ in range(self.expected_fans)]
        if web_get_all is not None:
            try:
                spd = web_get_all["fansSpeed"]
            except KeyError:
                pass
            else:
                round((int(spd) * 6000) / 100)
                for i in range(self.expected_fans):
                    fans[i].speed = spd

        return fans

    async def _get_errors(
        self, web_get_error_detail: dict = None
    ) -> List[MinerErrorData]:
        errors = []
        if web_get_error_detail is None:
            try:
                web_get_error_detail = await self.web.get_error_detail()
            except APIError:
                pass

        if web_get_error_detail is not None:
            try:
                # only 1 error?
                # TODO: check if this should be a loop, can't remember.
                err = web_get_error_detail["code"]
            except KeyError:
                pass
            else:
                err = int(err)
                if not err == 0:
                    errors.append(InnosiliconError(error_code=err))
        return errors

    async def _get_wattage_limit(self, web_get_all: dict = None) -> Optional[int]:
        if web_get_all:
            web_get_all = web_get_all["all"]

        if web_get_all is None:
            try:
                web_get_all = await self.web.get_all()
            except APIError:
                pass
            else:
                web_get_all = web_get_all["all"]

        if web_get_all is not None:
            try:
                level = web_get_all["running_mode"]["level"]
            except KeyError:
                pass
            else:
                # this is very possibly not correct.
                level = int(level)
                limit = 1250 + (250 * level)
                return limit
