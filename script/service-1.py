import time, os, signal


def sighandler(signum, frame):
    print("Signal TERM recieved, exiting ...")
    exit()


signal.signal(signal.SIGTERM, sighandler)

print("Starting process ...")

while True:
    print("Processing ...")
    time.sleep(1)
