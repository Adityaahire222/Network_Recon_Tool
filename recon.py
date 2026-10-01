import subprocess
import sys
import argparse
import json
import shutil
import logging


def setup_logging(log_file):
    if log_file:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )


def check_nmap():
    if shutil.which("nmap") is None:
        logging.error("Nmap is not installed or not in PATH.")
        print("[-] Error: Nmap is not installed or not in PATH.")
        sys.exit(1)


def check_host(target):
    logging.info(f"Starting host discovery for target: {target}")

    try:
        result = subprocess.run(
            ["nmap", "-sn", target],
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as error:
        logging.error(f"Host discovery failed: {error}")
        print(f"[-] Host discovery failed: {error}")
        sys.exit(1)

    if result.returncode != 0:
        logging.error("Nmap host discovery failed.")

        print("[-] Nmap host discovery failed.")

        if result.stderr.strip():
            logging.error(result.stderr.strip())
            print(f"    {result.stderr.strip()}")

        sys.exit(1)

    if "Host is up" in result.stdout:
        logging.info("Host discovery successful.")
        return True

    logging.warning("Host appears unreachable.")
    return False


def scan_ports(target, ports, scan_type):
    if scan_type == "service":
        nmap_args = ["nmap", "-sV", "-p", ports, target]
    else:
        nmap_args = ["nmap", "-p", ports, target]

    logging.info(
        f"Starting {scan_type} scan on {target}, ports: {ports}"
    )

    try:
        result = subprocess.run(
            nmap_args,
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as error:
        logging.error(f"Port scan failed: {error}")
        print(f"[-] Port scan failed: {error}")
        sys.exit(1)

    if result.returncode != 0:
        logging.error("Nmap port scan failed.")

        print("[-] Nmap port scan failed.")

        if result.stderr.strip():
            logging.error(result.stderr.strip())
            print(f"    {result.stderr.strip()}")

        sys.exit(1)

    logging.info("Port scan completed successfully.")

    return result.stdout


def parse_ports(nmap_output):
    ports = []

    for line in nmap_output.splitlines():
        parts = line.split()

        if len(parts) >= 3 and "/tcp" in parts[0]:
            port_info = {
                "port": parts[0],
                "state": parts[1],
                "service": parts[2],
                "version": " ".join(parts[3:]) if len(parts) > 3 else "-"
            }

            ports.append(port_info)

    logging.info(f"Parsed {len(ports)} TCP port result(s).")

    return ports


def save_json(output_file, target, scan_type, ports):
    report = {
        "target": target,
        "scan_type": scan_type,
        "ports": ports
    }

    try:
        with open(output_file, "w") as file:
            json.dump(report, file, indent=4)

    except OSError as error:
        logging.error(f"Could not save JSON report: {error}")
        print(f"[-] Could not save JSON report: {error}")
        sys.exit(1)

    logging.info(f"JSON report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Network Recon & Service Enumeration Tool"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "--ports",
        default="22,80,443,8000",
        help="Ports to scan (example: 22,80,443 or 1-100)"
    )

    parser.add_argument(
        "--scan",
        choices=["basic", "service"],
        default="service",
        help="Scan type: basic port scan or service/version detection"
    )

    parser.add_argument(
        "--output",
        help="Save scan results to a JSON file"
    )

    parser.add_argument(
        "--log",
        help="Save execution logs to a file"
    )

    args = parser.parse_args()

    setup_logging(args.log)

    logging.info("Network Recon Tool started.")

    check_nmap()

    target = args.target.strip()

    if not target:
        logging.error("Target cannot be empty.")
        print("[-] Error: Target cannot be empty.")
        sys.exit(1)

    ports_to_scan = args.ports.strip()

    if not ports_to_scan:
        logging.error("Port specification cannot be empty.")
        print("[-] Error: Port specification cannot be empty.")
        sys.exit(1)

    scan_type = args.scan
    output_file = args.output

    print("=" * 50)
    print("       NETWORK RECON TOOL v0.9")
    print("=" * 50)

    print(f"\nTarget: {target}")

    print("[+] Performing Nmap host discovery...")

    if not check_host(target):
        logging.error("Host appears unreachable.")
        print("[-] Host appears unreachable.")
        sys.exit(1)

    print("[+] Host is reachable")

    print(f"\n[+] Scan type: {scan_type}")
    print(f"[+] Scanning ports: {ports_to_scan}")

    output = scan_ports(
        target,
        ports_to_scan,
        scan_type
    )

    ports = parse_ports(output)

    print("\nPORT SCAN RESULTS")
    print("-" * 80)

    print(
        f"{'PORT':<10}"
        f"{'STATE':<12}"
        f"{'SERVICE':<12}"
        f"VERSION"
    )

    print("-" * 80)

    if not ports:
        logging.warning("No TCP port results found.")
        print("No TCP port results found.")

    for port in ports:
        print(
            f"{port['port']:<10}"
            f"{port['state']:<12}"
            f"{port['service']:<12}"
            f"{port['version']}"
        )

    if output_file:
        save_json(
            output_file,
            target,
            scan_type,
            ports
        )

        print(f"\n[+] Results saved to: {output_file}")

    if args.log:
        logging.info("Network reconnaissance completed.")
        print(f"[+] Log saved to: {args.log}")


if __name__ == "__main__":
    main()
