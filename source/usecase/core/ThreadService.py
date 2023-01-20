import threading
class ThreadService:

    def __init__(self) -> None:
        pass

    def set(self, key:str, value:any):
        setattr(threading.current_thread, key, value)

    def get(self, key:str)-> any:
        return getattr(threading.current_thread, key)        