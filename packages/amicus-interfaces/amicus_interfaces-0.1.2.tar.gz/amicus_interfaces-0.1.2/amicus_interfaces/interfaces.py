from abc import ABC, abstractmethod
from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom

class IObserver(ABC):

    @abstractmethod
    def notify(self, room:MatrixRoom, event:RoomMessageText, msg:str):
        pass

    @abstractmethod
    def prefix(self:str):
        pass


class IObservable(ABC):
    
    @abstractmethod
    def subscribe(self, observer: IObserver):
        pass

    @abstractmethod
    def unsubscribe(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, room:MatrixRoom, event:RoomMessageText, message: str, filepath: str= None, filename: str= None):
        pass


class IPlugin(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
    