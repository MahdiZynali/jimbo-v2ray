import socket
import time
import requests
from termcolor import colored, cprint

class scanner:
    '''test aliveness, upload speed, download speed'''

    def __init__(self, rangeIP, port, epoch, num_processes) -> None:
        self.rangeIP = rangeIP
        self.port = port
        self.epoch = epoch
        self.num_processes = num_processes
        self.ip_address = []
        self.generate_ip()
        self.scan_ips()

    def generate_ip(self):
        for ip in range(self.epoch):
            self.ip_address.append(self.rangeIP + str(ip))

    def ip_scanner(self, ip) -> bool:
        ''' check whether an IP is alive or not '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            res = sock.connect_ex((ip, 443))
            return res == 0
        except socket.error as e:
            print(f"Error scanning {ip}: {e}")
            return False
        finally:
            sock.close()

    def upload_speed(self, ip) -> None:
        ''' send packet into ip ip address to check upload speed time '''
        session_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.setdefaulttimeout(1)
        session_up.settimeout(1)
        packet = b"a" * 100000  # 0.1 MB of data
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as session_up:
                session_up.settimeout(1)
                session_up.connect((ip, 443))
                packet = b"a" * 100000  # 0.1 MB of data
                t0 = time.time()
                session_up.sendall(packet)
                session_up.recv(1024)  # Add this line to receive acknowledgment from the server
                upload_time_seconds = time.time() - t0
                cprint(f"Upload time: {upload_time_seconds:.6f} seconds", "blue")
                return upload_time_seconds
        except:
            cprint(f"Upload time : None", "blue")
            return False

    def download_speed(self, n_bytes: int, timeout: int, ips) -> None:
        ''' download initial amount of bytes from a specific address to check download speed time '''
        try:
            start_time = time.perf_counter()
            url = f"http://{ips}/__down"
            headers = {"Host": "speed.cloudflare.com"}
            params = {"bytes": n_bytes}

            r = requests.get(url, params=params, timeout=timeout, headers=headers)

            if r.status_code == 200:
                server_timing_header = r.headers.get("Server-Timing")
                if server_timing_header:
                    cf_time = float(server_timing_header.split("=")[1]) / 1000
                    total_time = time.perf_counter() - start_time
                    latency = r.elapsed.total_seconds() - cf_time
                    download_time = total_time - latency

                    mb = n_bytes * 8 / (10 ** 6)
                    download_speed = mb / download_time

                    cprint("Download speed: {:.2f} Mbps".format(download_speed), "blue")
                    return download_speed

            cprint("Download speed: None", "blue")
            return False

        except :
            cprint(f"Download speed: None", "blue")
            return False

    def handler(self, ip_address) -> None:
        ''' pass elements into processor functions and printout results'''
        print("Ip : ", ip_address)
        if self.ip_scanner(ip_address):
            up_speed = self.upload_speed(ip_address)
            down_speed = self.download_speed(1000000, timeout=2, ips=ip_address)
            if up_speed is not False and down_speed is not False:
                cprint("status : Alive", "green")
            else:
                cprint("Status : down", 'red')
            print("=" * 40)
        else:
            cprint("Status : down", 'red')
            print("=" * 40)

    def scan_ips(self):
        for ip_address in self.ip_address:
            self.handler(ip_address)