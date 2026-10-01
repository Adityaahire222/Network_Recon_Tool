# Network Recon & Service Enumeration Tool

A Python-based network reconnaissance tool that uses **Nmap** to perform host discovery, TCP port scanning, and basic service/version detection in an authorized lab environment.

## Features

* Host discovery using Nmap
* TCP port scanning
* Custom port selection
* Basic port scan
* Service and version detection
* Nmap output parsing
* JSON report generation
* Execution logging
* Input validation and error handling
* Command-line interface

## Technology Stack

* **Python 3**
* **Nmap**
* **Linux / Kali Linux**
* **Git**

## Project Structure

```text
network-recon-tool/
├── recon.py
├── README.md
├── .gitignore
└── __pycache__/
```

## Requirements

Make sure Python and Nmap are installed:

```bash
python3 --version
nmap --version
```

## Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd network-recon-tool
```

No external Python packages are required.

## Usage

Basic service scan:

```bash
python3 recon.py 127.0.0.1
```

Scan specific ports:

```bash
python3 recon.py 127.0.0.1 --ports 22,80,443,8000
```

Scan a port range:

```bash
python3 recon.py 127.0.0.1 --ports 1-100
```

### Scan Types

Basic port scan:

```bash
python3 recon.py 127.0.0.1 --ports 8000 --scan basic
```

Service/version detection:

```bash
python3 recon.py 127.0.0.1 --ports 8000 --scan service
```

## Reports and Logging

Save results as JSON:

```bash
python3 recon.py 127.0.0.1 --ports 8000 --output results.json
```

Save execution logs:

```bash
python3 recon.py 127.0.0.1 --ports 8000 --log recon.log
```

Both can be used together:

```bash
python3 recon.py 127.0.0.1 --ports 8000 --scan service --output results.json --log recon.log
```

## Workflow

```text
Target
  ↓
Host Discovery
  ↓
Port Scanning
  ↓
Service/Version Detection
  ↓
Nmap Output Parsing
  ↓
Terminal / JSON / Log
```

## Technical Concepts Covered

* Network reconnaissance
* Host discovery
* TCP port scanning
* Open, closed, and filtered ports
* Service/version detection
* Nmap output parsing
* Python subprocess execution
* CLI argument handling
* JSON reporting
* Logging
* Error handling and input validation
* Git version control

## Limitations

This is a learning-focused reconnaissance tool. It currently does not provide:

* UDP scanning
* Vulnerability scanning
* Exploitation
* Advanced web enumeration
* Automated vulnerability assessment

## Future Improvements

Possible future additions include:

* UDP scanning
* HTML report generation
* HTTP service enumeration
* DNS enumeration
* Automated test cases
* Additional Nmap scan options

## Authorized Use

This tool is intended for **authorized security testing, personal labs, and educational purposes only**.

Only scan systems that you own or have explicit permission to test.
