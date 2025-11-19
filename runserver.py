import os
import sys
import subprocess

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_shop.settings")
    subprocess.call([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
