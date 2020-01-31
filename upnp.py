import threading
import socket

import config


class UPNPResponderThread(threading.Thread):
    UPNP_RESPONSE = """HTTP/1.1 200 OK
CACHE-CONTROL: max-age=60
EXT:
LOCATION: http://{0}:{1}/description.xml
SERVER: FreeRTOS/6.0.5, UPnP/1.0, IpBridge/0.1
ST: urn:schemas-upnp-org:device:basic:1
USN: uuid:Socket-1_0-221438K0100073::urn:schemas-upnp-org:device:basic:1

""".format(config.get('network.listen_ip'), config.get('network.http_port')).replace("\n", "\r\n").encode('utf-8')

    stop_thread = False

    def run(self):
        # Listen for UDP port 1900 packets sent to SSDP multicast address
        print("UPNP Responder Thread started...")
        ssdpmc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Required for receiving multicast
        ssdpmc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssdpmc_socket.setsockopt(
            socket.SOL_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(config.get('network.listen_ip'))
        )
        ssdpmc_socket.setsockopt(
            socket.SOL_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton("239.255.255.250") + socket.inet_aton(config.get('network.listen_ip'))
        )

        ssdpmc_socket.bind(("239.255.255.250", 1900))

        while True:
            try:
                data, addr = ssdpmc_socket.recvfrom(1024)
            except socket.error as e:
                if self.stop_thread:
                    print("UPNP Reponder Thread closing socket and shutting down...")
                    ssdpmc_socket.close()
                    return
                print("UPNP Responder socket.error exception occured: {0}".format(e.__str__))

            # SSDP M-SEARCH method received - respond to it unicast with our info
            if "M-SEARCH" in data.decode('utf-8'):
                print("UPNP Responder sending response to {0}:{1}".format(addr[0], addr[1]))
                ssdpout_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ssdpout_socket.sendto(self.UPNP_RESPONSE, addr)
                ssdpout_socket.close()

    def stop(self):
        self.stop_thread = True
