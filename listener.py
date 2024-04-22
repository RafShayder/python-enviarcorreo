import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        new_file = event.src_path
        print(f"Se ha creado un archivo: {new_file}")

    def on_modified(self, event):
        modified_file = event.src_path
        
        if event.is_directory:
            return
        if event.event_type == 'modified':
            time.sleep(1)  # Agregamos un retraso de 1 segundo
            print(f"Se ha modificado un archivo: {modified_file}")

if __name__ == "__main__":
    folder_to_watch = "./inputvariable/"

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
