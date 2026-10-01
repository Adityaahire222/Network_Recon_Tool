import subprocess
import sys
import argparse
import json
import shutil


def check_nmap():
    if shutil.which("nmap") is None:
        print("[-] Error: Nmap is not installed or not in PATH.")
        sys.exit(1)


def check_host(target):
    try:
        result = subprocess.run(
            ["nmap", "-sn", target],
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as error:
        print(f"[-] Host discovery failed: {error}")
        sys.exit(1)

    if result.returncode != 0:
        print("[-] Nmap host discovery failed.")
        if result.stderr.strip():
            print(f"    {result.stderr.strip()}")
        sys.exit(1)

    return "Host is up" in result.stdout


def scan_ports(target, ports, scan_type):
    if scan_type == "service":
        nmap_args = ["nmap", "-sV", "-p", ports, target]
    else:
        nmap_args = ["nmap", "-p", ports, target]

    try:
        result = subprocess.run(
            nmap_args,
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as error:
        print(f"[-] Port scan failed: {error}")
        sys.exit(1)

    if result.returncode != 0:
        print("[-] Nmap port scan failed.")
        if result.stderr.strip():
            print(f"    {result.stderr.strip()}")
        sys.exit(1)

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
        print(f"[-] Could not save JSON report: {error}")
        sys.exit(1)


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

    args = parser.parse_args()

    check_nmap()

    target = args.target.strip()

    if not target:
        print("[-] Error: Target cannot be empty.")
        sys.exit(1)

    ports_to_scan = args.ports.strip()

    if not ports_to_scan:
        print("[-] Error: Port specification cannot be empty.")
        sys.exit(1)

    scan_type = args.scan
    output_file = args.output

    print("=" * 50)
    print("       NETWORK RECON TOOL v0.8")
    print("=" * 50)

    print(f"\nTarget: {target}")

    print("[+] Performing Nmap host discovery...")

    if not check_host(target):
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


if __name__ == "__main__":
    main()
