import subprocess
import unittest


class TestNetworkConnectivity(unittest.TestCase):
    def get_public_ip(self):
        # Get public IP address using OpenDNS
        result = subprocess.run(
            ['host', 'myip.opendns.com', 'resolver1.opendns.com'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception("Failed to get public IP")

        # Extract the public IP from the command output
        ip_lines = result.stdout.splitlines()
        public_ip = ip_lines[-1].split()[-1] if len(ip_lines) > 5 else None
        
        return public_ip

    def ping(self, host):
        # Ping the specified host and return the response time and packet loss
        try:
            result = subprocess.run(
                ['ping', '-c', '1', host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                return None, None

            # Extract the time and packet loss from the output
            lines = result.stdout.splitlines()
            if len(lines) > 1:
                time_line = lines[1]
                loss_line = lines[4]
                
                # Extract time and packet loss
                time_ms = time_line.split('time=')[-1].split()[0]  # Get the time in ms
                packet_loss = loss_line.split()[5]  # Get packet loss

                return time_ms, packet_loss
            else:
                return None, None
        except Exception as e:
            print(f"Error pinging {host}: {e}")
            return None, None

    def test_network_connectivity(self):
        public_ip = self.get_public_ip()
        self.assertIsNotNone(public_ip, "Failed to retrieve public IP")

        url = f"{public_ip}:5000"

        net_millisec, net_packet = self.ping("google.com")
        self.assertIsNotNone(net_millisec, "Failed to ping google.com")
        
        net_packet_loss = self.ping(url)[1]
        self.assertIsNotNone(net_packet_loss, f"Failed to ping {url}")

        if int(net_millisec) > 0 and net_packet_loss:
            print(f"\nIt took {net_millisec} ms to reach {url} and there was {net_packet_loss} data packet loss.")
        else:
            print("\nYour website cannot be reached. Check your configuration.")

if __name__ == "__main__":
    unittest.main()
