import time
from os import system
from datetime import datetime


def service():
    now = datetime.now()
    while True:
        time.sleep(30)
        # if the hour is  between 1hour and 3hour,
        # we are going to reboot
        if 1 <= now.hour <= 3:
            system("sudo reboot")

        print(f"{now} : stand by...")
        time.sleep(3600)


if __name__ == "__main__":
    print("reboot service started")
    service()
