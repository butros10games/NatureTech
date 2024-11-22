import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_restart = time.time()

    def on_any_event(self, event):
        if time.time() - self.last_restart < 5:  # 10 seconds cooldown
            return

        if event.is_directory:
            return

        if (
            event.event_type == "modified"
            and (event.src_path.endswith(".py") or event.src_path.endswith(".html"))
            and not event.src_path.endswith("manage.py")
        ):
            print("Python file change detected, restarting uWSGI...")
            subprocess.run(["sudo", "systemctl", "reload", "uwsgi-NatureTech.service"])
            self.last_restart = time.time()

        ## check if the changed file is in the static_workfile folder
        if event.event_type == "modified" and event.src_path.startswith(
            "/home/butros/NatureTech/static_workfile"
        ):
            print("Static file change detected, restarting nginx...")
            subprocess.run(
                [
                    "/home/butros/NatureTech_env/bin/python",
                    "/home/butros/NatureTech/manage.py",
                    "collectstatic",
                    "--noinput",
                ]
            )
            self.last_restart = time.time()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
