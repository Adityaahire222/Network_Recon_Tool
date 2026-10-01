import subprocess
import sys
import argparse


def check_host(target):
    result = subprocess.run(
        ["nmap", "-sn", target],
        capture_output=True,
        text=True
    )

    return "Host is up" in result.stdout


def scan_ports(target, ports, scan_type):
    if scan_type == "service":
        nmap_args = ["nmap", "-sV", "-p", ports, target]
    else:
        nmap_args = ["nmap", "-p", ports, target]

    result = subprocess.run(
        nmap_args,
        capture_output=True,
        text=True
    )

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

    args = parser.parse_args()

    target = args.target
    ports_to_scan = args.ports
    scan_type = args.scan

    print("=" * 50)
    print("       NETWORK RECON TOOL v0.6")
    print("=" * 50)

    print(f"\nTarget: {target}")

    print("[+] Performing Nmap host discovery...")

    if not check_host(target):
        print("[-] Host appears unreachable")
        sys.exit(1)

    print("[+] Host is reachable")

    print(f"\n[+] Scan type: {scan_type}")
    print(f"[+] Scanning ports: {ports_to_scan}")

    output = scan_ports(target, ports_to_scan, scan_type)

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

    for port in ports:
        print(
            f"{port['port']:<10}"
            f"{port['state']:<12}"
            f"{port['service']:<12}"
            f"{port['version']}"
        )


if __name__ == "__main__":
    main()
