from abc import ABC, abstractmethod
from Event import Event


class Observer(ABC):

    @abstractmethod
    def update(self, event: Event):
        pass
        """接收到通知时，由观察者执行的操作"""


pass
