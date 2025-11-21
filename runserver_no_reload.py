import os
import sys
import threading
import time
import multiprocessing
import socket
from django.core.management import execute_from_command_line

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize


def is_port_open(host, port):
    """Check if a port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def wait_for_server(host="127.0.0.1", port=8000, timeout=20):
    """Wait until Django server is ready."""
    print(">> Waiting for Django server to start...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_port_open(host, port):
            print(">> Django server is running!")
            return True
        time.sleep(0.5)

    print(">> ERROR: Django server failed to start!")
    return False


def start_django():
    """Start the Django server."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_shop.settings")

    args = ["manage.py", "runserver", "127.0.0.1:8000", "--noreload", "--nothreading"]
    execute_from_command_line(args)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("E-Shop Application")
        self.setGeometry(100, 100, 1280, 800)
        self.setMinimumSize(QSize(800, 600))

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))


def main():
    # Start Django server thread
    django_thread = threading.Thread(target=start_django, daemon=True)
    django_thread.start()

    # Wait until server is READY
    wait_for_server()

    # Start PyQt window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()