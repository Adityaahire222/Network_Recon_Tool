import subprocess
import sys


def check_host(target):
    result = subprocess.run(
        ["nmap", "-sn", target],
        capture_output=True,
        text=True
    )

    return "Host is up" in result.stdout


def scan_ports(target, ports):
    result = subprocess.run(
        ["nmap", "-sV", "-p", ports, target],
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
    if len(sys.argv) != 2:
        print("Usage: python3 recon.py <target>")
        sys.exit(1)

    target = sys.argv[1]

    print("=" * 50)
    print("       NETWORK RECON TOOL v0.4")
    print("=" * 50)

    print(f"\nTarget: {target}")

    print("[+] Performing Nmap host discovery...")

    if not check_host(target):
        print("[-] Host appears unreachable")
        sys.exit(1)

    print("[+] Host is reachable")

    print("\n[+] Scanning ports: 22,80,443,8000")

    output = scan_ports(target, "22,80,443,8000")

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
