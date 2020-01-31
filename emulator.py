import webserver
from upnp import UPNPResponderThread

if __name__ == "__main__":
    UPNPResponderThread().start()
    webserver.run()
