# Python Port Scanner

A simple and educational Python-based network port scanner for legitimate security testing and network administration purposes.

## What is a Port Scanner?

A port scanner is a network security tool that probes a host or server for open ports. Open ports can indicate which services are running on a target system, helping network administrators verify their security configurations and identify potential vulnerabilities.

**How it works:**
- Attempts to establish TCP connections to specified ports on a target host
- If a connection is successful, the port is considered "open"
- Maps common port numbers to their associated services (e.g., port 22 → SSH, port 80 → HTTP)
- Can scan ranges of ports sequentially or using multiple threads for faster scanning

## Features

- ✅ Interactive command-line interface
- ✅ Support for IP addresses and hostnames
- ✅ Customizable port ranges
- ✅ Both sequential and multithreaded scanning modes
- ✅ Service identification for common ports
- ✅ Comprehensive error handling
- ✅ Clean, readable output format
- ✅ Built-in timeout management

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only built-in modules)

## Installation

1. Clone or download the script:
```bash
git clone <repository-url>
cd python-port-scanner
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x port_scanner.py
```

## Usage

### Basic Usage

```bash
python port_scanner.py
```

The script will prompt you for:
- Target IP address or hostname
- Port range (optional, defaults to 1-1024)
- Whether to use multithreading (optional, defaults to yes)

### Example Interactive Session

```
==============================================================
           PYTHON PORT SCANNER
==============================================================
Note: This tool is for educational and authorized testing only.
Ensure you have permission to scan the target system.

Enter target IP address or hostname: scanme.nmap.org
Enter port range (default 1-1024): 1-100
Use threading? (y/n, default y): y

Starting scan at 2024-01-15 14:30:22
Resolved scanme.nmap.org to 45.33.32.156

Starting threaded scan on 45.33.32.156
Scanning ports 1-100 with 100 threads
--------------------------------------------------
Port 22/tcp open - SSH
Port 80/tcp open - HTTP

Threaded scan completed in 2.45 seconds

==============================================================
SCAN RESULTS SUMMARY
==============================================================
Host: scanme.nmap.org (45.33.32.156)
Open ports found: 2

PORT    STATE   SERVICE
------------------------------
22/tcp  open    SSH
80/tcp  open    HTTP
==============================================================
```

### Programmatic Usage

You can also use the PortScanner class in your own Python scripts:

```python
from port_scanner import PortScanner

# Create scanner instance
scanner = PortScanner("192.168.1.1", start_port=1, end_port=1000)

# Run threaded scan
scanner.run(use_threading=True)

# Access results
for port, service in scanner.open_ports:
    print(f"Found {service} on port {port}")
```

## Configuration Options

The `PortScanner` class accepts several parameters:

- `target`: IP address or hostname to scan
- `start_port`: Starting port number (default: 1)
- `end_port`: Ending port number (default: 1024)
- `timeout`: Connection timeout in seconds (default: 1)
- `max_threads`: Maximum concurrent threads (default: 100)

## Supported Services

The scanner can identify these common services:

| Port | Service | Port | Service |
|------|---------|------|---------|
| 20 | FTP-DATA | 21 | FTP |
| 22 | SSH | 23 | TELNET |
| 25 | SMTP | 53 | DNS |
| 80 | HTTP | 110 | POP3 |
| 143 | IMAP | 443 | HTTPS |
| 993 | IMAPS | 995 | POP3S |
| 3306 | MySQL | 3389 | RDP |
| 5432 | PostgreSQL | 6379 | Redis |

## Performance Comparison

- **Sequential scanning**: Slower but more reliable, good for detailed scans
- **Multithreaded scanning**: Much faster, suitable for quick reconnaissance

Example performance on a typical network:
- Sequential scan (1-1024 ports): ~45-60 seconds
- Threaded scan (1-1024 ports): ~3-8 seconds

## Legal and Ethical Considerations

⚠️ **IMPORTANT DISCLAIMER**

This tool is provided for educational and legitimate security testing purposes only. Users must:

1. **Only scan systems you own or have explicit permission to test**
2. **Comply with all applicable laws and regulations**
3. **Respect network policies and terms of service**
4. **Use responsibly and ethically**

Unauthorized port scanning may be considered:
- A violation of computer crime laws
- Network abuse or reconnaissance activity  
- Grounds for account termination by ISPs

The authors are not responsible for any misuse of this tool.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Performance improvements
- Additional service mappings
- Documentation improvements
- New features

## License

This project is released under the MIT License. See LICENSE file for details.

## Troubleshooting

### Common Issues

1. **"Unable to resolve hostname"**
   - Check internet connection
   - Verify hostname spelling
   - Try using IP address instead

2. **No open ports found on known active host**
   - Host may have firewall blocking connections
   - Try increasing timeout value
   - Check if host actually has services running

3. **Slow scanning performance**
   - Reduce number of concurrent threads
   - Increase timeout value
   - Check network connection quality

4. **Permission errors**
   - Some systems require administrator privileges
   - Try running with elevated permissions if needed

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Open an issue on GitHub with details about your problem
4. Include Python version, OS, and error messages when reporting bugs
