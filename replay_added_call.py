import queue
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class ReplayHandler(FileSystemEventHandler):
    def __init__(self,queue):
        self.queue = queue
    
    def on_created(self, event: FileSystemEvent) -> None:
        self.queue.put(event.src_path)

def ReplayAdded(initiaPath, on_replay):
    queue1 = queue.Queue()
    event_handler = ReplayHandler(queue1)
    observer = Observer()

    observer.schedule(event_handler, initiaPath, recursive=True)
    observer.start()
    try:
        while True:
            path = queue1.get()
            try:
                on_replay(path)
            except Exception as e:
                print(f"Error processing {path}: {e}")
    finally:
        observer.stop()
        observer.join()
        

