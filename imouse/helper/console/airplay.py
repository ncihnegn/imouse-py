from typing import TYPE_CHECKING, List, Optional

from ...types import SetDeviceAirplayParams
from ...models import ImServerConfigData

if TYPE_CHECKING:
    from imouse.helper.console import Console
    from imouse import API


class AirPlay:
    def __init__(self, console: "Console"):
        self._console = console
        self._api: "API" = console._helper._api

    def _require_config(self) -> ImServerConfigData:
        config = self._console.get_imserver_config
        if config is None:
            raise ValueError("获取内核配置失败")
        return config

    def global_config(
            self,
            fps: Optional[int] = None,
            ratio: Optional[int] = None,
            audio: Optional[bool] = None,
            img_fps: Optional[int] = None
    ) -> bool:
        """设置 iMouse 全局 AirPlay 配置（用于所有设备默认使用）"""
        config = self._require_config()
        update_map = {
            'air_play_fps': fps,
            'air_play_ratio': ratio,
            'air_play_audio': audio,
            'air_play_img_fps': img_fps,
        }
        for key, value in update_map.items():
            if value is not None:
                setattr(config, key, value)
        return self._console.successful(self._api.config_imserver_set(config))

    def config(
            self,
            device_ids: str,
            fps: Optional[int] = None,
            ratio: Optional[int] = None,
            refresh: Optional[int] = None,
            audio: Optional[int] = None,
            img_fps: Optional[int] = None
    ) -> bool:
        """设置指定设备的 AirPlay 配置"""
        params = SetDeviceAirplayParams()
        if fps is not None:
            params["fps"] = fps
        if ratio is not None:
            params["ratio"] = ratio
        if refresh is not None:
            params["refresh"] = refresh
        if audio is not None:
            params["audio"] = audio
        if img_fps is not None:
            params["img_fps"] = img_fps
        return self._console.successful(self._api.device_airplay_set(device_ids, params))

    def connect(self, device_ids: str) -> bool:
        """指定设备的投屏"""
        return self._console.successful(self._api.device_airplay_connect(device_ids))

    def connect_all(self) -> bool:
        """让所有离线的设备投屏"""
        return self._console.successful(self._api.device_airplay_connect_all())

    def disconnect(self, device_ids: str) -> bool:
        """断开指定设备的投屏"""
        return self._console.successful(self._api.device_airplay_disconnect(device_ids))

    def name(self, name: str) -> bool:
        """设置 AirPlay 的显示名称"""
        config = self._require_config()
        config.air_play_name = name
        return self._console.successful(self._api.config_imserver_set(config))

    def auto_connect(self, state: bool) -> bool:
        """设置是否自动连接设备"""
        config = self._require_config()
        config.auto_connect = state
        return self._console.successful(self._api.config_imserver_set(config))

    def failed_retry(self, num: int) -> bool:
        """设置连接失败后的重试次数"""
        config = self._require_config()
        config.connect_failed_retry = num
        return self._console.successful(self._api.config_imserver_set(config))

    def gpu_decoding(self, state: bool) -> bool:
        """设置是否启用 GPU 硬件解码"""
        config = self._require_config()
        config.enable_hardware_acceleration = state
        return self._console.successful(self._api.config_imserver_set(config))

    def set_mdns_type(self, mdns_type: int, ip_list: Optional[List[str]] = None) -> bool:
        """设置 mDNS 类型及允许的 IP 列表"""
        config = self._require_config()
        config.mdns_type = mdns_type
        if ip_list is not None:
            config.allow_ip_list = ip_list

        return self._console.successful(self._api.config_imserver_set(config))

    def restart_mdns(self) -> bool:
        """重新广播投屏"""
        return self._console.successful(self._api.imserver_regmdns())
