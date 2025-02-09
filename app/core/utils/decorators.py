import threading

def singleton(cls):
    """Decorator to make a class singleton with thread-safe."""
    instances = {}
    lock = threading.Lock()  # Thread lock

    def get_instance(*args, **kwargs):
        with lock: 
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance