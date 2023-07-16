import serial.tools.list_ports
import win32com.client
import threading
import pythoncom
import pywintypes

from abc import ABC, abstractmethod
from Logger import LoggerMetaclass
from typing import Any, Type, Callable
from Event import Event
from Observer import Observer


class Port:

    def __init__(self, name: str, description: str):
        """
        description作为设备唯一区分
        """
        self.name = name
        self.description = description

    def __eq__(self, other):
        if isinstance(other, Port):
            return self.description == other.description
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class DeviceMonitor(threading.Thread):

    def __init__(self, On_device_added: Callable, On_device_removed: Callable):
        """
        串口设备监视器

        Args:
            On_device_added (Callable): Plugged device callback function.
            On_device_removed (Callable): Unplugged device callback function.
        """
        super().__init__(daemon=True)
        self.device_added_callback = On_device_added
        self.device_removed_callback = On_device_removed
        self._stop_event = threading.Event()
        # self.device_manager = device_manager

    def __getattribute__(self, __name: str) -> Any:
        """
        实例方法调用捕获

        Args:
            __name (str):

        Returns:
            Method of being decorated.
        """
        attr = super().__getattribute__(__name)
        if callable(attr):
            return self.logger.log_exceptions(attr)
        return attr

    def stop(self):
        self._stop_event.set()

    def run(self):
        """
        设备监听线程
        """
        pythoncom.CoInitialize()  # 初始化 COM
        try:
            # 创建 WMI 服务对象
            wmi = win32com.client.GetObject("winmgmts:")

            # 创建事件查询
            watcher = wmi.ExecNotificationQuery(
                "SELECT * FROM __InstanceOperationEvent WITHIN 0.5 WHERE TargetInstance ISA 'Win32_USBControllerdevice'"
            )

            while not self._stop_event.is_set():
                try:
                    event = watcher.NextEvent(1000)  # 设置超时，以便在停止事件被设置时能及时退出
                    device_id = event.TargetInstance.Dependent.split('=')[-1]
                    if event.Path_.Class == "__InstanceCreationEvent":
                        # self.device_manager.device_added(device_id)
                        self.device_added_callback(device_id)
                    elif event.Path_.Class == "__InstanceDeletionEvent":
                        # self.device_manager.device_removed(device_id)
                        self.device_removed_callback(device_id)

                except pywintypes.com_error as e:
                    if e.hresult == -2147352567:

                        continue
                    else:
                        raise e
        finally:
            pythoncom.CoUninitialize()  # 反初始化 COM


class DeviceManager(ABC, metaclass=LoggerMetaclass):

    def __getattribute__(self, __name: str) -> Any:
        """
        实例方法调用捕获

        Args:
            __name (str):

        Returns:
            Method of being decorated.
        """
        attr = super().__getattribute__(__name)
        if callable(attr):
            return self.logger.log_exceptions(attr)
        return attr

    @abstractmethod
    def add_observer(self, observer: Observer):
        """添加观察者"""

    @abstractmethod
    def remove_observer(self, observer: Observer):
        """移除观察者"""

    @abstractmethod
    def notify_observers(self, event_data):
        """当有事件发生时，通知所有的观察者"""


class SerialDeviceManager(DeviceManager):

    def __init__(self, devices_focus: list[str]):
        """
        Args:
            devices_focus (list[str]): 需要关注的设备的描述的关键字列表，如通讯芯片
        """
        self.devices_focus = devices_focus
        self.observers = set()  # 用于存储观察者
        self._last_device = None
        self.devices = self.get_connected_devices()
        self.device_monitor_thread = DeviceMonitor(self.device_added,
                                                   self.device_removed)
        self.device_monitor_thread.start()

    def add_observer(self, observer: Type[Observer]):
        """
        TODO: Observers to add: TUI, Uploader, Replacer
        """
        self.observers.add(observer)

    def remove_observer(self, observer: Type[Observer]):
        self.observers.remove(observer)

    def notify_observers(self, event_data: dict):
        """

        Args:
            event_data (dict): 插入或拔出的设备，{行为类型: 设备}
        """
        for observer in self.observers:
            event = Event("device_changes", event_data)
            observer.update(event)

    def get_connected_devices(self) -> set[Port]:
        """获取当前连接的设备并按self.devices筛选"""
        ports_set = set(serial.tools.list_ports.comports())
        return {
            Port(port.name, keyword)
            for port in ports_set
            for keyword in self.devices_focus if keyword in port.description
        }  # 筛选掉多余的设备

    def device_added(self, device_id):
        new_devices = self.get_connected_devices()
        added_device = new_devices - self.devices
        if added_device:
            device = added_device.pop()
            if self._last_device and device == self._last_device:
                # reconnected
                self.notify_observers({"reconnected": device})
            else:
                # new device added
                self.notify_observers({"connected": device})
        self.devices = new_devices

    def device_removed(self, device_id):
        new_devices = self.get_connected_devices()
        removed_device = self.devices - new_devices
        if removed_device:
            device = removed_device.pop()
            # disconnected
            self.notify_observers({"disconnected": device})
            self._last_device = device
        self.devices = new_devices

    def check_device_changes(self):
        """检查设备变化，并通知所有观察者"""
        updated_devices = self.get_connected_devices()
        if updated_devices != self.current_devices:
            event_data = {
                'connected': updated_devices - self.current_devices,
                'disconnected': self.current_devices - updated_devices
            }
            self.current_devices = updated_devices
            self.notify_observers(event_data)


pass
