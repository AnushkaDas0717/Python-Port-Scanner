#!/usr/bin/env python3
"""
Simple Port Scanner
A basic Python-based network port scanner for educational and legitimate security testing purposes.
"""

import socket
import threading
import time
import sys
from datetime import datetime

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1, max_threads=100):
        """
        Initialize the port scanner
        
        Args:
            target (str): Target IP address or hostname
            start_port (int): Starting port number
            end_port (int): Ending port number
            timeout (int): Connection timeout in seconds
            max_threads (int): Maximum number of threads for concurrent scanning
        """
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.lock = threading.Lock()
        
        # Common service mappings
        self.service_map = {
            20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
            53: "DNS", 69: "TFTP", 80: "HTTP", 110: "POP3", 119: "NNTP",
            123: "NTP", 143: "IMAP", 161: "SNMP", 194: "IRC", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 3389: "RDP", 5432: "PostgreSQL",
            3306: "MySQL", 1521: "Oracle", 1433: "MSSQL", 6379: "Redis",
            27017: "MongoDB", 5672: "RabbitMQ", 9200: "Elasticsearch"
        }
    
    def resolve_target(self):
        """
        Resolve hostname to IP address and validate target
        
        Returns:
            str: Resolved IP address
        
        Raises:
            socket.gaierror: If hostname cannot be resolved
        """
        try:
            ip = socket.gethostbyname(self.target)
            print(f"Resolved {self.target} to {ip}")
            return ip
        except socket.gaierror:
            raise socket.gaierror(f"Unable to resolve hostname: {self.target}")
    
    def scan_port(self, port):
        """
        Scan a single port
        
        Args:
            port (int): Port number to scan
            
        Returns:
            bool: True if port is open, False otherwise
        """
        try:
            # Create socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Attempt connection
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            
            # Connection successful if result is 0
            return result == 0
            
        except socket.error:
            return False
    
    def threaded_scan(self, port):
        """
        Thread worker function for scanning ports
        
        Args:
            port (int): Port number to scan
        """
        if self.scan_port(port):
            service = self.service_map.get(port, "Unknown")
            with self.lock:
                self.open_ports.append((port, service))
                print(f"Port {port}/tcp open - {service}")
    
    def scan_sequential(self):
        """
        Perform sequential port scanning (single-threaded)
        """
        print(f"\nStarting sequential scan on {self.target_ip}")
        print(f"Scanning ports {self.start_port}-{self.end_port}")
        print("-" * 50)
        
        start_time = time.time()
        
        for port in range(self.start_port, self.end_port + 1):
            if self.scan_port(port):
                service = self.service_map.get(port, "Unknown")
                self.open_ports.append((port, service))
                print(f"Port {port}/tcp open - {service}")
        
        end_time = time.time()
        print(f"\nSequential scan completed in {end_time - start_time:.2f} seconds")
    
    def scan_threaded(self):
        """
        Perform multithreaded port scanning
        """
        print(f"\nStarting threaded scan on {self.target_ip}")
        print(f"Scanning ports {self.start_port}-{self.end_port} with {self.max_threads} threads")
        print("-" * 50)
        
        start_time = time.time()
        threads = []
        
        # Create and start threads
        for port in range(self.start_port, self.end_port + 1):
            # Limit concurrent threads
            while len([t for t in threads if t.is_alive()]) >= self.max_threads:
                time.sleep(0.01)
            
            thread = threading.Thread(target=self.threaded_scan, args=(port,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        print(f"\nThreaded scan completed in {end_time - start_time:.2f} seconds")
    
    def print_results(self):
        """
        Print scan results summary
        """
        print("\n" + "="*60)
        print("SCAN RESULTS SUMMARY")
        print("="*60)
        
        if self.open_ports:
            # Sort ports by number
            self.open_ports.sort(key=lambda x: x[0])
            
            print(f"Host: {self.target} ({self.target_ip})")
            print(f"Open ports found: {len(self.open_ports)}")
            print("\nPORT\tSTATE\tSERVICE")
            print("-" * 30)
            
            for port, service in self.open_ports:
                print(f"{port}/tcp\topen\t{service}")
        else:
            print(f"No open ports found on {self.target} ({self.target_ip})")
        
        print("="*60)
    
    def run(self, use_threading=True):
        """
        Main scanning function
        
        Args:
            use_threading (bool): Whether to use multithreaded scanning
        """
        try:
            # Resolve target
            self.target_ip = self.resolve_target()
            
            # Clear previous results
            self.open_ports = []
            
            # Perform scan
            if use_threading:
                self.scan_threaded()
            else:
                self.scan_sequential()
            
            # Print results
            self.print_results()
            
        except socket.gaierror as e:
            print(f"Error: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nScan interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

def main():
    """
    Main function with user interaction
    """
    print("="*60)
    print("           PYTHON PORT SCANNER")
    print("="*60)
    print("Note: This tool is for educational and authorized testing only.")
    print("Ensure you have permission to scan the target system.")
    print("")
    
    try:
        # Get target from user
        target = input("Enter target IP address or hostname: ").strip()
        if not target:
            print("Error: No target specified")
            return
        
        # Get port range (optional)
        port_range = input("Enter port range (default 1-1024): ").strip()
        if port_range:
            try:
                if '-' in port_range:
                    start_port, end_port = map(int, port_range.split('-'))
                else:
                    start_port = end_port = int(port_range)
            except ValueError:
                print("Invalid port range. Using default 1-1024")
                start_port, end_port = 1, 1024
        else:
            start_port, end_port = 1, 1024
        
        # Get scan method
        method = input("Use threading? (y/n, default y): ").strip().lower()
        use_threading = method != 'n'
        
        # Create and run scanner
        scanner = PortScanner(target, start_port, end_port)
        
        print(f"\nStarting scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        scanner.run(use_threading)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
