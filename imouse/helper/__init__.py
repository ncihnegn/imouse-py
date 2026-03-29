from typing import List, Optional

import imouse
from .device import Device
from .console import Console
from ..models import DeviceInfo


class Helper:
    def __init__(self, api: imouse.API):
        self._api = api

    @property
    def console(self):
        return Console(self)

    def device(self, device_id: str, device_info: Optional[DeviceInfo] = None) -> Device:
        return Device(self, device_id, device_info)

    @property
    def devices(self) -> List[Device]:
        device_list_response = self._api.device_get()
        if device_list_response is None or not device_list_response.data.device_list:
            return []
        ret: List[Device] = []
        for data in device_list_response.data.device_list:
            ret.append(self.device('', data))
        return ret
